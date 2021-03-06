#!/bin/bash 
export LC_ALL="C.UTF-8"
BASE_DIR="/home/adabalap/Source/telugu_padyalu"


clean_up_stale_process() {
	#
	# Clean up and stale process from previous run
	#
	echo
	stale_process="Xvfb chromedriver"

	for i in $stale_process
	do
  		echo "`date`: Checking for ${i} stale process"
  		ps -ef | grep ${i} | grep -v grep

  		if [[ $? == 1 ]]
  		then
    			echo "`date`: No ${i} stale process found"
  		else
    			echo "`date`: Cleaning up ${i} stale process"
    			/usr/bin/pkill ${i}
    			sleep 5
  		fi
	done
}

main() {
	# Main function
	clean_up_stale_process
	python3 telugu_padyalu.py	-m whatsapp \
            		          	-u "😎Family😎" \
                               	-d ./telugu_padyalu.DB \
		    	            	-c "☀️ శుభోదయం ☀️"
	return $?
}

# Setup the environment and run the program
cd ${BASE_DIR}
. ${BASE_DIR}/venv/bin/activate

RETRY="True"
SLEEP_TIME=300
RETRY_COUNT=0

while [ "$RETRY" == "True" ]
do
	main
	rc=$?	

	if [[ $rc -eq 0 && $RETRY_COUNT -eq 0 ]]; then
		echo "`date`: Delivered message on first attempt"
		RETRY="False"
		break
 	elif [[ $rc -ne 0 && $RETRY_COUNT -eq 0 ]]; then	
		# initialize the retry start time
		RETRY_START_TIME=`date`	
	fi
	
	# Applying rate limit logic for retry
	# Sleep for 5 minutes before retry
	# 1. retry every 5 minutes in the 1st hour
	# 2. retry evey 1 hour thereafer for next 3 hours
	echo
	echo "`date`: Sleeping for ${SLEEP_TIME} before retrying"
	echo "`date`: Current retry count is ${RETRY_COUNT}"
	echo

	sleep ${SLEEP_TIME}
	RETRY_COUNT=$(($RETRY_COUNT + 1))


	if [[ ${RETRY_COUNT} -eq 11 ]]; then
		# sleep for 1 hour before retrying
		SLEEP_TIME=$((60 * 60))
	fi
	
	if [[ ${RETRY_COUNT} -ge 15 ]]; then
		# retried from 4AM to 8AM 
		RETRY_END_TIME=`date`	
		echo "`date`: Performed retry from ${RETRY_START_TIME} to ${RETRY_END_TIME}"
		RETRY="False"
		break
	fi
done

deactivate
