import acsploit
import exploits
import inspect
import re
import cmd
import input

class cmdline(cmd.Cmd):

    intro = "\n**********ACsploit**********\n"
    prompt = "(acsploit) "
    origpromptlen = len(prompt)
    options = dict({"exploit" : "", "input" : "", "attack" : "time"})
    currexp = None
    currinputgen = None
    availexps = {}
    
    def init(self):
        for name, obj in inspect.getmembers(exploits, inspect.isclass):
            try:
                arg_name = re.sub("Exploit", '', name).lower()
                self.availexps[arg_name] = obj
            except TypeError:
                pass

    def do_EOF(self, args):
        return True

    def do_options(self, args):
        for key, option in self.options.items():
            print "  " + key + ": " +  str(option)
        if self.currexp != None:
            print "\n  Exploit options:"
            for key, option in self.currexp.options.items():
                print "    " + key + ": " +  str(option)
        if self.options["input"] != "":
            print "\n  Input options:"
            for key, option in self.currinputgen.options.items():
                print "    " + key + ": " +  str(option)

    def do_set(self, args):
        args = args.split()
        if len(args) < 2:
            return

        key = args[0]
        val = args[1]

        if key == "exploit":
            self.update_exploit(val)
        elif key == "input":
            #TODO check input
            self.options["input"] = val
            if val == "int":
                self.currinputgen = input.IntGenerator()
            if val == "char":
                self.currinputgen = input.CharGenerator()
            if val == "string":
                self.currinputgen = input.StringGenerator()
        elif (self.currexp != None) and (key in self.currexp.options):
            #TODO check input type is what is expected?
            self.currexp.options[key] = val
        elif (self.currinputgen != None) and (key in self.currinputgen.options):
            #TODO check input type is what is expected?
            self.currinputgen.options[key] = val
        else:
            print("Option "+ key+ " does not exist.")

    def update_exploit(self, expname):
        if expname in self.availexps:
            self.prompt = self.prompt[:self.origpromptlen - 2] + ":"+expname+") "
            self.currexp = self.availexps[expname]
            self.options["exploit"] = expname
        else:
            print("Exploit " + expname + " does not exist.")
            pass

    def do_run(self, args):
        #TODO
        if self.currexp != None:
            self.currexp().run(self.currinputgen) 
        else:
            #TODO print error
            pass

if __name__ == '__main__':
    cmdlineobj = cmdline()
    cmdlineobj.init()
    cmdline().cmdloop()
