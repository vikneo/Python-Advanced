# Иерархия исключений

```html
BaseException  
|___Exception  
|      |______TypeError  
|      |______StopAsyncIteration  
|      |______StopIteration  
|      |______ImportError  
|      |         |_________ModuleNotFoundError   
|      |         |_________ZipImportError        
|      |______OSError  
|      |         |_________ConnectionError       
BrokenPipeError  
ConnectionAbortedError  
ConnectionRefusedError  
ConnectionResetError  
|      |         |_________BlockingIOError       
|      |         |_________ChildProcessError     
|      |         |_________FileExistsError       
|      |         |_________FileNotFoundError     
|      |         |_________IsADirectoryError     
|      |         |_________NotADirectoryError    
|      |         |_________InterruptedError      
|      |         |_________PermissionError       
|      |         |_________ProcessLookupError    
|      |         |_________TimeoutError          
|      |         |_________UnsupportedOperation  
|      |______EOFError  
|      |______RuntimeError  
|      |         |_________RecursionError        
|      |         |_________NotImplementedError   
|      |         |__________DeadlockError        
|      |______NameError  
|      |         |_________UnboundLocalError     
|      |______AttributeError  
|      |______SyntaxError  
|      |         |_________IndentationError  
TabError  
|      |______LookupError  
|      |         |_________IndexError  
|      |         |_________KeyError  
|      |         |_________CodecRegistryError  
|      |______ValueError  
|      |         |_________UnicodeError  
UnicodeEncodeError  
UnicodeDecodeError  
UnicodeTranslateError  
|      |         |_________UnsupportedOperation  
|      |______AssertionError  
|      |______ArithmeticError  
|      |         |_________FloatingPointError  
|      |         |_________OverflowError  
|      |         |_________ZeroDivisionError  
|      |______SystemError  
|      |         |_________CodecRegistryError  
|      |______ReferenceError  
|      |______MemoryError  
|      |______BufferError  
|      |______Warning  
|      |         |_________UserWarning  
|      |         |_________EncodingWarning  
|      |         |_________DeprecationWarning  
|      |         |_________PendingDeprecationWarning  
|      |         |_________SyntaxWarning  
|      |         |_________RuntimeWarning  
|      |         |_________FutureWarning  
|      |         |_________ImportWarning  
|      |         |_________UnicodeWarning  
|      |         |_________BytesWarning  
|      |         |_________ResourceWarning  
|      |_______OptionError  
|      |______error  
|      |______Verbose  
|      |______Error  
|      |______TokenError  
|      |______StopTokenizing  
|      |______ClassFoundException  
|      |______EndOfBlock  
|___GeneratorExit  
|___SystemExit  
|___KeyboardInterrupt  
```