#!/usr/bin/env python
import os
import sys

# check that GnuPG is installed                                                                                                                                                                       
def which(program):
    """
    A implementation of the "which" utility in Linux originally written in Perl and 
    was contributed by Wolfram Schneider. This specific implementation 
    was written by Jay Loden (http://jayloden.com/) and was sourced from a stackoverflow 
    answer (http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python)
    """
    import os                                                                                                                                                                                         

    def is_exe(fpath):                                                                                                                                                                                
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)                                                                                                                                    

    fpath, fname = os.path.split(program)                                                                                                                                                             

    if fpath:                                                                                                                                                                                         
        if is_exe(program):                                                                                                                                                                          
            return program                                                                                                                                                                            
    else:                                                                                                                                                                                             
        for path in os.environ["PATH"].split(os.pathsep):                                                                                                                                             
            path = path.strip('"')                                                                                                                                                                    
            exe_file = os.path.join(path, program)                                                                                                                                                    
            if is_exe(exe_file):                                                                                                                                                                      
                return exe_file                                                                                                                                                                       

    return None 

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mayan.settings.local")

    if which('gpg') is None:                                                                                                                                                                          
        raise EnvironmentError('GnuPG is required to install Mayan EDMS, please visit https://www.gnupg.org/download/ to get GnuPG')    

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
