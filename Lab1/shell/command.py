import readline
class Completer(object):
    def __init__(self):
        self.__commands = []
        self.__has_arg = {}

    def register(self, command_obj):
        self.__commands.append(command_obj.cmd)
        self.__has_arg[command_obj.cmd] = command_obj.has_arg
        if command_obj.has_arg:
            setattr(self, 'complete_{}'.format(
                command_obj.cmd), command_obj.complete)

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        lines = buffer.split()
        # show all commands
        if not lines:
            if state >= len(self.__commands):
                return None
            else:
                return self.__commands[state]
        cmd = lines[0]
        if cmd in self.__commands:
            if not self.__has_arg[cmd]:
                return None
            if len(lines) == 1 and buffer[-1] != ' ':
                if state == 0:
                    return cmd + ' '
                else:
                    return None
            f = getattr(self, 'complete_{}'.format(cmd))
            args = lines[1:]
            return (f(args, buffer[-1]) + [None])[state]
        results = []
        for c in self.__commands:
            if c.startswith(cmd):
                # has arg end with space
                if self.__has_arg[c]:
                    results.append(c + ' ')
                else:
                    results.append(c)
        results.append(None)
        return results[state]


class Command(object):
    def __init__(self, shell, cmd, has_arg):
        self.cmd = cmd
        self.has_arg = has_arg
        self.shell = shell

    def complete(self, args, end):
        return []

    def parse(self, cmds):
        pass


class CommandCr(Command):
    def __init__(self, shell):
        super().__init__(shell, 'cr', True)

    def complete(self, args, end):
        if len(args) == 1:
            if end != ' ':
                return [args[0] + ' ']
            else:
                return ['1', '2']
        return []

    def parse(self, cmds):
        if len(cmds) != 2:
            print('cr error: only has 2 arg')
            return
        name = cmds[0]
        try:
            priority = int(cmds[1])
        except ValueError:
            priority = None
        if priority != 1 and priority != 2:
            print('cr error: priority should be 1 or 2')
            return
        if self.shell.create_process(name, priority, 0): # bug
            print('* Process {} is running'.format(name))
        else:
            print('cr error: process {} exists'.format(name))


class CommandDe(Command):
    def __init__(self, shell):
        super().__init__(shell, 'de', True)

    def complete(self, args, end):
        if len(args) == 0:
            args = ['']
        pname_list = self.shell.get_pname_dict().keys()
        if args[0] in pname_list:
            return []
        return [c for c in pname_list if c.startswith(args[0])]

    def parse(self, cmds):
        if len(cmds) != 1:
            print('de error: only has 1 arg')
            return
        pname = cmds[0]
        pname_list = self.shell.get_pname_dict()
        if pname not in pname_list:
            print('de error: no such process named {}'.format(pname))
            return
        self.shell.delete_process(pname_list[pname])
        print('* Process {} has been delete'.format(pname))

class CommandPr(Command):
    def __init__(self, shell):
        super().__init__(shell, 'pr', True)

    def complete(self, args, end):
        if len(args) == 0:
            args = ['']
        pname_list = self.shell.get_pname_dict().keys()
        if args[0] in pname_list:
            return []
        return [c for c in pname_list if c.startswith(args[0])]

    def parse(self, cmds):
        if len(cmds) != 1:
            print('pr error: only has 1 arg')
            return
        pname = cmds[0]
        pname_list = self.shell.get_pname_dict()
        if pname not in pname_list:
            print('pr error: no such process named {}'.format(pname))
            return
        pcb = self.shell.process_list[pname_list[pname]].pcb
        print('pid: {}'.format(pcb.pid))
        print('name: {}'.format(pcb.name))
        print('status: {}'.format(pcb.status))
        print('priority: {}'.format(pcb.priority))
        print('parent: {}'.format(pcb.parent))
        print('children: {}'.format(pcb.children))
        print('queue: {}'.format(pcb.queue))



class CommandList(Command):
    def __init__(self, shell):
        super().__init__(shell, 'list', True)
        self.__commands = {'ready': self.shell.list_ready,
                          'block': self.shell.list_block, 'res': self.shell.list_res}

    def complete(self, args, end):
        if len(args) > 1:
            return []
        if not args:
            args = ['']
        if args[0] in self.__commands:
            return []
        return [c for c in self.__commands if c.startswith(args[0])]

    def parse(self, cmds):
        if len(cmds) != 1:
            print('list error: only has 1 arg')
            return
        if cmds[0] in self.__commands:
            self.__commands[cmds[0]]()
        else:
            print('list error: arg error')


class CommandTo(Command): # todo
    def __init__(self, shell):
        super().__init__(shell, 'to', False)

    def parse(self, cmds):
        if len(cmds) != 0:
            print('to error: only has not arg')
            return
        self.shell.clock_interrupt()


class CommandReq(Command):
    def __init__(self, shell):
        super().__init__(shell, 'req', True)

    def complete(self, args, end):
        if len(args) == 0:
            args = ['']
        resource_list = self.shell.resources.rcbs
        resource_name_list = ['R{}'.format(c.rid) for c in resource_list]

        if len(args) == 1:
            if args[0] in resource_name_list:
                if end == ' ':
                    return []
                else:
                    return [args[0] + ' ']
            else:
                return [c + ' ' for c in resource_name_list if c.startswith(args[0])]
        return []

    def parse(self, cmds):
        if len(cmds) != 2:
            print('req error: only has 2 arg')
            return
        rname = cmds[0]
        rnum = cmds[1]
        try:
            rid = int(rname[1:])
            if rid < 1 or rid > 4:
                raise ValueError()
        except ValueError:
            print('req error: rid error')
            return
        try:
            rnum = int(rnum)
        except ValueError:
            print('req error: rnum error')
            return
        self.shell.request(self.shell.running_process, rid, rnum)
        
class CommandRel(Command):
    def __init__(self, shell):
        super().__init__(shell, 'rel', True)

    def complete(self, args, end):
        if len(args) == 0:
            args = ['']
        resource_list = self.shell.resources.rcbs
        resource_name_list = ['R{}'.format(c.rid) for c in resource_list]

        if len(args) == 1:
            if args[0] in resource_name_list:
                if end == ' ':
                    return []
                else:
                    return [args[0] + ' ']
            else:
                return [c + ' ' for c in resource_name_list if c.startswith(args[0])]
        return []

    def parse(self, cmds):
        if len(cmds) != 2:
            print('rel error: only has 2 arg')
            return
        rname = cmds[0]
        rnum = cmds[1]
        try:
            rid = int(rname[1:])
            if rid < 1 or rid > 4:
                raise ValueError()
        except ValueError:
            print('rel error: rid error')
            return
        try:
            rnum = int(rnum)
        except ValueError:
            print('rel error: rnum error')
            return
        self.shell.release(self.shell.running_process, rid, rnum)

command_list = [CommandPr, CommandList, CommandCr, CommandDe, CommandTo, CommandReq, CommandRel]