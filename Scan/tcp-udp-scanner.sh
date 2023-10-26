#!/usr/bin/env bash

# Package installation
apt install -y libnotify-bin parallel

# Creating the results directory
mkdir -p scans

# Check the arguments
if [ $# -eq 0 ]; then
    echo "Uso: bash scan.parallel.sh <ips.txt> [#jobs]"
    exit 1
fi

# Defines the variables
TARGETS=$1
JOBS=${2:-""}

# TCP Scan
echo "Iniciando varredura TCP com $JOBS trabalhos"
parallel -j$JOBS --ungroup --bar -a $TARGETS --max-args 1 \
    'echo TCP: Job {#} of {= $_=total_jobs() =} - {} && \
    echo "scan.parallel.sh" "iniciando TCP - {#} / {= $_=total_jobs() =} - {}" && \
    nmap -A -p- -v --reason -T5 -sS --script "(default or safe or vuln or discovery) and not broadcast" -oA scans/{}.tcp {}'

# UDP Scan
echo "Iniciando varredura UDP com $JOBS trabalhos (top 50 portas)"
parallel -j$JOBS --ungroup -a $TARGETS --max-args 1 \
    'echo UDP: Job {#} of {= $_=total_jobs() =} - {} && \
    echo "scan.parallel.sh" "iniciando UDP - {#} / {= $_=total_jobs() =} - {}" && \
    nmap -sU -sV -T4 --top-ports 50 -oA scans/{}.udp {}' &

wait

echo "Concluído!"
