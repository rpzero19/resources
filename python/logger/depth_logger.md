# How to collect, customize, and centralize Python logs
- from [datagoghq](https://www.datadoghq.com/blog/python-logging-best-practices/)
- https://stackoverflow.com/questions/25187083/python-logging-to-multiple-handlers-at-different-log-levels
- 
## Key Points
- we can setup logging by `basicConfig()`
- But frameworks like Django and Flask use file based-dictionary based logging configuration.


## Now Digging deeper into Python’s logging library

As your application scales, you’ll need a more robust, scalable way to configure each module-specific logger—and to make sure you’re capturing the logger name as part of each log. In this section, we’ll explore how to:
 - configure multiple loggers and automatically capture the logger name
 - use fileConfig() to implement custom formatting and routing options
 - capture tracebacks and uncaught exceptions

### Configure multiple loggers and automatically capture the logger name
- best practice of creating a new logger for each module in your application,
    
- `logger = logging.getLogger(__name__)`Use this, orelse every log will get logged in root, and difficult to debug



### Use fileConfig() to output logs to multiple destinations:
A logging configuration file needs to contain three sections:

- [loggers]: the names of the loggers you’ll configure.
- [handlers]: the handler(s) these loggers should use (e.g., consoleHandler, fileHandler).
- [formatters]: the format(s) you want each logger to follow when generating a log.

Each section should include a comma-separated list of one or more keys: keys=handler1,handler2,[...]. 

The keys determine the names of the other sections you’ll need to configure, formatted as [<SECTION_NAME>_<KEY_NAME>], where the section name is logger, handler, or formatter. 

A Simple logging configuration file(logging,ini)

```
[loggers]
keys=root

[handlers]
keys=fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=fileHandler

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=("/path/to/log/file.log",)

[formatter_simpleFormatter]
format=%(asctime)s %(name)s - %(levelname)s:%(message)s
```

IMP NOTE:
Python’s logging documentation recommends that you should only attach each handler to one logger and rely on propagation to apply handlers to the appropriate child loggers. 

This means that if you have a default logging configuration that you want all of your loggers to pick up, you should add it to a parent logger (such as the root logger), rather than applying it to each lower-level logger. 

See the [documentation](https://docs.python.org/3/library/logging.html#logging.Logger.propagate) for more details about propagation.



#### In this example, we configured a root logger and let it propagate to both of the modules in our application (lowermodule and uppermodule).

```commandline
import logging.config

logging.config.fileConfig('/path/to/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
```

In this example, disable_existing_loggers is set to False,  indicating that the logging module should not disable pre-existing non-root loggers. 

This setting defaults to True, which will disable any non-root loggers that existed prior to fileConfig() unless you configure them afterward.


### Python exception handling and tracebacks


We should use `exc_info=True` or `logger.exception` for full traceback error
```commandline
except OSError as e:
        logger.error(e)
        logger.error(e, exc_info=True)
        
 or
 except OSError as e:
        logger.exception(e, exc_info=True)      
```


#### Capturing unhandled exceptions

An unhandled exception occurs outside of a try...except block, or when you don’t include the correct exception type in your except statement. 

For instance, if your application encounters a TypeError exception, and your except clause only handles a NameError, it will get passed to any remaining try clauses until it encounters the correct exception type.

If it does not, it becomes an unhandled exception, 
in which case, the interpreter will invoke sys.excepthook(), with three arguments: 
- the exception class, 
- the exception instance, and 
- the traceback. 

This usually appears in `sys.stderr` but if you’ve configured your logger to output to a file, the traceback information won’t get logged there.

So, we can use Python’s standard traceback library to format the traceback and include it in the log message.

```commandline
# lowermodule.py
import logging.config
import traceback

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def word_count(myfile):
    try:
        # count the number of words in a file, myfile, and log the result
        with open(myfile, 'r+') as f:
            file_data = f.read()
            words = file_data.split(" ")
            final_word_count = len(words)
            logger.info("this file has %d words", final_word_count)
            f.write("this file has %d words", final_word_count)
            return final_word_count
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False

if __name__ == '__main__':
    word_count('myfile.txt')
    
```
