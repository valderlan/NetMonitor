#!/bin/bash

interface=$1
output_dir=$2
user=$3
rotate_interval=60

[[ "$(grep -c "$interface" /proc/net/dev)" == "0" ]] && echo "The interface is NOT found!" && exit 255
[[ ! -d "$output_dir" ]] && echo "The output directory does NOT exist!" && exit 255

# Clean
cleanup() {
	echo "=== Capturer is being cancled ==="
    echo "=== Wait the converter finished for 3 seconds..."
	sleep 3
	echo 
	echo "=== Convert left PCAP files if any"
	OIFS="$IFS"
	IFS=$'\n'
	for f in `find "${output_dir}" -type f -name "*.pcap"`; do
		echo "=== $f is left"
		"${post_rotate_command}" "$f"
	done
	IFS="$OIFS"

    echo "=== Clean stuff up"
    rm -f "$output_dir"/*.pcap

	echo 
    exit 0
}

trap 'cleanup' INT TERM EXIT

#output_file=${output_dir}/$(date +'%Y-%m-%d-%H:%M:%S.pcap')
output_file_format=${output_dir}/'%Y-%m-%d-%H:%M:%S.pcap'
options="-n -nn -N -s 0"

[[ ! -z "${user}" ]] && options="${options} -Z ${user}"  #$(id -nu 1000)

# Before the post-rotatation script can be run, please edit an AppArmor configuration file:
#   $ sudo vi /etc/apparmor.d/usr.sbin.tcpdump
# by adding the line:
#   /**/* ixr,
# then
#   $ sudo service apparmor restart
#
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # On the same directory.
post_rotate_command="${script_dir}"/convert_pcap_csv.sh

sudo tcpdump ${options} -z "${post_rotate_command}" -i ${interface} -G ${rotate_interval} -w "${output_file_format}"

# -z postrotate-command
# Observe que o tcpdump executará o comando paralelamente à captura, usando a prioridade mais baixa para que isso não perturbe o processo de captura.
# E caso você queira usar um comando que aceite bandeiras ou argumentos diferentes, você sempre pode escrever um shell script que use o 
# nome do arquivo de salvamento como o único argumento, faça as bandeiras &argumentos e execute o comando que você deseja.
# -G rotate_seconds
# Se especificado, gira o arquivo de despejo especificado com a opção -w a cada rotate_seconds segundos. 
# Os arquivos de salvamento têm o nome especificado por -w, que deve incluir um formato de hora, conforme definido por strftime . 
# Se nenhum formato de hora for especificado, cada novo arquivo substituirá o anterior.

#sudo chown 1000:1000 "${output_dir}"/*

