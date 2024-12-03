#! /bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/sbin/apt-cacher-ng
NAME=apt-cacher-ng
DESC=apt-cacher-ng
USER=apt-cacher-ng
GROUP=apt-cacher-ng

test -x $DAEMON || exit 0

# Include apt-cacher-ng defaults if available
if [ -f /etc/default/apt-cacher-ng ] ; then
        . /etc/default/apt-cacher-ng
fi

# our runtime state files directory, will be purged on startup!
RUNDIR="/var/run/$NAME"

PIDFILE="$RUNDIR/pid"
SOCKETFILE="$RUNDIR/socket"
DAEMON_OPTS="$DAEMON_OPTS pidfile=$PIDFILE SocketPath=$SOCKETFILE foreground=1"

# start apt-cacher-ng daemon
chmod 2755 /var/cache/apt-cacher-ng /var/log/apt-cacher-ng
chown $USER:$GROUP /var/cache/apt-cacher-ng /var/log/apt-cacher-ng
rm -rf "$RUNDIR" || return 1
install -d --mode=0755 -o $USER -g $GROUP "$RUNDIR" || return 1
start-stop-daemon --start --chuid $USER --group $GROUP --quiet --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
