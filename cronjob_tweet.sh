#!/bin/bash 
export LC_ALL="C.UTF-8"
BASE_DIR="/home/adabalap/Source/telugu_padyalu"

cd ${BASE_DIR}
. ${BASE_DIR}/venv/bin/activate

#python3 telugu_padyalu.py  -m twitter \
#                    -d ./telugu_padyalu.DB \
#                    -t ./cfg/twitter_tokens.json \
#                    -ht "#తెలుగుపద్యాలు #పద్యాలు #వేమనపద్యాలు #వేమనశతకం #వేమన" \
#                    -T test
echo "`date`: ${0} : Posting tweet"
python3 telugu_padyalu.py -m twitter \
                   -d ./telugu_padyalu.DB \
                   -t ./cfg/twitter_tokens.json \
                   -ht "#తెలుగుపద్యాలు #పద్యాలు #సుమతీశతకము #సుమతీపద్యాలు #సుమతీ"

if [[ $? == 0 ]]
then
	echo "`date`: ${0} : Posted tweet"
else
	echo "`date`: ${0} : rc = ${?}, Check something went wrong"
fi
	
deactivate

