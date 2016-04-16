# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

ORACLE_SID="lsomop"
export ORACLE_SID

# User specific aliases and functions
PATH=./:${HOME}/bin:$PATH:/usr/bin
export PATH

CDPATH=./:../:${HOME}
export CDPATH

export SQLPATH="${HOME}/sqlPlusInit"
export PS1='`whoami`@.../${PWD##*/}>'
alias ls='ls -F'
alias ll='ls -l'
