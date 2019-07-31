"""
The Judge class is responsible for executing the submitted
source code on test cases, and return final result: pass/fail
"""
from problem import Problem, SolutionError
import signal, os
import threading

TIMEOUT = 2
class TimeoutError(Exception):
    "Raised when the execution time out"

def timeout_handler(signum, frame):
    raise TimeoutError("Time Exceeded when executing your solution")

class Judge(object):
    def __init__(self, problem_id, src, mode="inline"):
        problems = Problem.load_problemset()
        self.src = src
        self.problem = None
        for problem in problems:
            if problem._id == problem_id:
                self.problem = problem
        self.error = None
        if mode=="inline":
            self.executor = self.inline_execute
        else: # mode == "thread"
            self.executor = self.thread_execute
        
    def run_tests(self):
        if not self.problem:
            return False, "Problem not found."
        for raw_in, raw_out in self.problem.tests:
            # get input ready
            _input = self.problem.prepare_input(raw_in)
            # execute this test case
            try:
                ret, _output = self.executor(_input)
            except Exception as e: # A guard for uncaught exception in execution
                return False, str(e)
            else:
                if not ret:
                    return ret, _output
                else:
                    # Execution is successful, validate if result is correct
                    try:
                        correct = self.problem.validate_result(raw_in, _input, raw_out, _output)
                    except Exception, e:
                        return False, str(e)
                    if not correct:
                        error_str = "Result incorrect for input %s, your output: %s"%(raw_in, self.problem.get_output_str(_output))
                        return False, error_str
        # Now all tests passed
        return True, None
                
    def inline_execute(self, _in):
        context = {}
        try:
            code = compile(self.src, "<submitted code>", "exec")
        except SyntaxError, e:
            return False, str(e)
        try:
            exec code in context
        except Exception as e:
            return False, str(e)
        if "Solution" not in context or \
            not callable(context['Solution']):
            return False, "Solution class not found in solution code."

        solution = context['Solution']()
        try:
            method = getattr(solution, self.problem.method_name)
        except AttributeError as e:
            return False, "Method %s not found"%self.problem.method_name

        # use alarm to monitor TLE, only *nix system support timeout alarm
        if hasattr(signal, "SIGALRM"):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(1)

        sb = Sandbox()
        sb.enter_sandbox()
        try:
            if isinstance(_in, tuple):
                _out = method(*_in)
            else:
                _out = method(_in)
        except TimeoutError as e:
            return False, "Time limit exceeded when executing your code"
        except Exception as e:
            return False, str(e)
        finally:
            sb.exit_sandbox()
            if hasattr(signal, "alarm"):
                signal.alarm(0) # cancel the alarm

        return True, _out

    def thread_execute(self, _in):
        # these 2 variables will be set by the thread
        _result = []
        _exception = []
        
        def runner():
            context = {}
            try:
                code = compile(self.src, "<submitted code>", "exec")
            except SyntaxError, e:
                _exception.append(e)
                raise
            try:
                exec code in context
            except Exception as e:
                _exception.append(e)
                raise
            
            if "Solution" not in context or \
                not callable(context['Solution']):
                e = SolutionError("Solution class not found in solution code.")
                _exception.append(e)
                raise e
            
            
            solution = context['Solution']()
            try:
                method = getattr(solution, self.problem.method_name)
            except AttributeError as e:
                _exception.append(e)
                raise

            sandbox = Sandbox()
            sandbox.enter_sandbox()
            try:
                if isinstance(_in, tuple):
                    _out = method(*_in)
                else:
                    _out = method(_in)
            except Exception as e:
                _exception.append(e)
                sandbox.exit_sandbox()
                raise
            finally:
                sandbox.exit_sandbox()

            _result.append(_out)
            
        t = threading.Thread(target=runner)
        t.start()
        t.join(TIMEOUT)
        if t.isAlive():
            return False, "Time limit exceeded when executing your code"
        elif _exception:
            return False, str(_exception[0])
        else:
            return True, _result[0]


class SecurityError(Exception):
    "Raised when the execution violates sandbox restriction"

class SafeModule:
        def __getattr__(self, attrname):
            return Sandbox.jail

# This sandbox is inspired by this link: https://isisblogs.poly.edu/2012/10/26/escaping-python-sandboxes/        
class Sandbox(object):
    @staticmethod
    def jail(*args):
        raise SecurityError("You are trying to violate sandbox security")

    def __init__(self):
        self._builtins = {}
        self.os_module = None
        self.subprocess_module = None
        
    def enter_sandbox(self):
        UNSAFE = [
            'file',
            'execfile',
            'compile',
            'reload',
            'eval',
            'input'
        ]
        import __builtin__
        for func in UNSAFE:
            self._builtins[func] = __builtin__.__dict__[func]
            __builtin__.__dict__[func] = self.jail

        import sys
        import os
        import subprocess
        self.os_module = sys.modules['os']
        self.subprocess_module = sys.modules['subprocess']
        sys.modules['os'] = SafeModule()
        sys.modules['subprocess'] = SafeModule()

    def exit_sandbox(self):
        import __builtin__
        __builtin__.__dict__.update(self._builtins)
        import sys
        sys.modules['os'] = self.os_module
        sys.modules['subprocess'] = self.subprocess_module
        
        
        
 
        
            
        
