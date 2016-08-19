#!/bin/bash

# Usage: script.sh <log file location> <options>
#

# Get Shell variables

COLUMN_LENGTH=$(tput cols)


# Define Horiontal line
H_BAR=$(printf "%*s\n" ${COLUMN_LENGTH} | tr " " "=")

# Define initial variables

LOG_ANALYSIS_DIRECTORY="/tmp/log_analysis/"
LOG_ONLY_LOCATION="/tmp/log_analysis/log_only"
DIAGNOSTIC_INFO_LOCATION="/tmp/log_analysis/diagnostic_info_only"
LOG_ANALYSIS_RESULT="/tmp/log_analysis/analysis_result"
DEFAULT_KEYWORDS="\->\|<-\|Result:\|No such unix\|INFO\|WARN\|ERR\|Failed\|userauth-request"
DEFAULT_EXCLUDED_KEYWORDS="AUDIT_TRAIL\|SendATProxySetAuditTrailEventVAList"
MODE="OVERVIEW" # Default parsing mode.
WORD_EXCLUDE_FLAG=FALSE

# Define Functions.
# Check execution status. 0 = good. non-zero = exit 3.

CHECK_EXIT ()
	{
		case ${?} in
			0)
				#echo " Successfully $1 $2"
			;;
			*)
				EXIT_STATUS=${?}
				echo "Error. Could not $1 $2"
				exit ${EXIT_STATUS}
			;;
		esac
	}

# Clean up after exit.
CLEAN_UP ()
	{
		rm -rf ${LOG_ONLY_LOCATION}
		rm -rf ${DIAGNOSTIC_INFO_LOCATION}
	}



# Get Options.
# h or ? = usage
# s = Parse logs from this line
# e = Log Parse ends here. If not specified, the end of file is assumed. 
# t = exclude keywords. Separated by space. Like this "word1 word2 word3"

OPTIND=1       # Reset to 1 just in case.

while getopts "h?s:e:t:" OPTIONS; do
	case ${OPTIONS} in
		h|"?")
			echo -e " Usage: script.sh <options> <log file>. \n -s = begining of line. -e = end of line. \n -t = Exclude specified keywrods"
			exit 0
		;;

		s)
			BEGIN_LINE=${OPTARG}
			MODE="LINE_PARSE"
			echo "Parsing from line # ${BEGIN_LINE}"
		;;

		e)
			END_LINE=${OPTARG}
			MODE="LINE_PARSE"
			echo "Parsing to line # ${END_LINE}"
		;;

		t)
			EXCLUDE_KEYWORDS=${OPTARG}
			echo "Excluding the following keywords: ${EXCLUDE_KEYWORDS}"
			# for KEYWORD in ${EXCLUDE_KEYWORDS}; do
			# 	echo "Excluded word ${KEYWORD}"
			# done
			WORD_EXCLUDE_FLAG=TRUE
		;;

		*)
			echo "Invalid otion -${OPTARG}} was used"
			echo -e " Usage: script.sh <log file> <options>. \n- s = begining of line. -e = end of line"
			exit 1
		;;
	esac
done

# Line Parse mode. 
# Verify entered values are valid before coninuing. 

if [ ${MODE} == "LINE_PARSE" ]
	then
		if [ ! -z ${BEGIN_LINE} ] && [ ! -z ${END_LINE} ]  && [ ${BEGIN_LINE} -lt ${END_LINE} ] ## Needs improvement. Consider if entered values are not integers.
			then
				echo "Valid line numbers"
		else
			echo "Invalid line numbers"
			exit 1
		fi
fi

LOGFILELOCATION=${@:${OPTIND}:1} ## Log file is assumed to be presented at

#
# If words to exclude are specified, replace spaces with '\|' for use with grep later.

if [ WORD_EXCLUDE_FLAG == TRUE ]
 	then
		EXCLUDE_KEYWORDS=$(echo ${EXCLUDE_KEYWORDS} | sed 's: :\\|:g' )
fi



# Validation Steps. If error occurs during tehse steps, return code will be 1.
#
#Ensure files are okay:

# case ${1} in

	# ' ')
		# echo " Usage: script.sh <log file> <options>"
	# ;;

	# *)
		# if [ -f ${LOGFILELOCATION} ]; then
			# echo "Found ${LOGFILELOCATION}, processing"
			# if [[ "$(file ${LOGFILELOCATION}  -b)" == *"ASCII text, with very long lines"*  ]]; then ## Needs improvement.
				LOGFILE=${LOGFILELOCATION}
				echo "${LOGFILE} will be used"
			# else
				# echo "Unsupported file. Only ASCII text file is supported"
				# exit 1
			# fi
		# else
			# echo "Log file ${LOGFILELOCATION} not found"
			# exit 1
		# fi
	# ;;
# esac

# Separate logs from the rest of the content.
# Saved to /tmp/log_analysis/log_only file. This should be deleted upon script exit.
#


if [ ! -d ${LOG_ANALYSIS_DIRECTORY} ];
	then 
	mkdir -p ${LOG_ANALYSIS_DIRECTORY}
fi 


LOG_START=$(grep -n -e '^/var/log/centrifydc.log\|^System logging information' ${LOGFILE} | cut -f1 -d:)
sed -n "${LOG_START},\$p" ${LOGFILE} > ${LOG_ONLY_LOCATION}
sed -n "1,${LOG_START}p" ${LOGFILE} > ${DIAGNOSTIC_INFO_LOCATION}
CHECK_EXIT create ${LOG_ONLY_LOCATION}
CHECK_EXIT create ${DIAGNOSTIC_INFO_LOCATION}


# Begin Writing to ${LOG_ANALYSIS_RESULT}
# Start parsing texts in the log file.


echo ${H_BAR} > ${LOG_ANALYSIS_RESULT} # This overrides any existing analysis result. 
echo ${H_BAR} >> ${LOG_ANALYSIS_RESULT}



# Basic Environmental checks
# Get current DC, computer account info, keytab info. 
#Possible Performance impact. May need to separate diagnostic information from logs. 


CURRENT_DC=$(grep "Current DC" ${DIAGNOSTIC_INFO_LOCATION}  -m1 | tr -s ' ' | cut -d " " -f3)

echo -e "Basic Environmental Checks \n" >> ${LOG_ANALYSIS_RESULT}
grep "Join Status:" ${DIAGNOSTIC_INFO_LOCATION}  -A 20 -m1 >> ${LOG_ANALYSIS_RESULT}
grep  "Domain Controller: ${CURRENT_DC}:"  -m2 ${DIAGNOSTIC_INFO_LOCATION} -A6 >> ${LOG_ANALYSIS_RESULT}
echo "" >> ${LOG_ANALYSIS_RESULT}
sed -n '/Computer\ Account/,/^$/p' ${DIAGNOSTIC_INFO_LOCATION} >> ${LOG_ANALYSIS_RESULT}
echo "Last machine password update: " >> ${LOG_ANALYSIS_RESULT}
sed -n   '/Keytab\ name:/,/^$/p' ${DIAGNOSTIC_INFO_LOCATION} | tail -n6 >> ${LOG_ANALYSIS_RESULT}
echo " NSS Config:" >> ${LOG_ANALYSIS_RESULT}
grep -e "^passwd:\|^group:\|^shadow:\|^hosts:" ${DIAGNOSTIC_INFO_LOCATION} >> ${LOG_ANALYSIS_RESULT} 
echo -e " \n adclient configuration" >> ${LOG_ANALYSIS_RESULT} 
sed -n '/Configuration:/,/^$/p' ${DIAGNOSTIC_INFO_LOCATION} >> ${LOG_ANALYSIS_RESULT}



#DIAG_LINE_B=$(grep -n -m1 '========Domain info map========' ${LOGFILE})
#DIAG_LINE_E=${}



echo ${H_BAR} >> ${LOG_ANALYSIS_RESULT}
echo ${H_BAR} >> ${LOG_ANALYSIS_RESULT}

if [ ${WORD_EXCLUDE_FLAG} == FALSE ] ; then

	case ${MODE} in
		OVERVIEW)
			echo -e "Overview: \n " >> ${LOG_ANALYSIS_RESULT}
			grep -n "${DEFAULT_KEYWORDS}" ${LOG_ONLY_LOCATION}  | grep -v "${DEFAULT_EXCLUDED_KEYWORDS}" >> ${LOG_ANALYSIS_RESULT}
			echo -e " \n    Parsed logs are stored in ${LOG_ANALYSIS_RESULT} \n"
		;;

		LINE_PARSE)
			echo "Displaying from line ${BEGIN_LINE} to ${END_LINE}"
			sed -n "${BEGIN_LINE},${END_LINE}p" ${LOG_ONLY_LOCATION} >> ${LOG_ANALYSIS_RESULT}
			echo -e " \n    Parsed logs are stored in ${LOG_ANALYSIS_RESULT} \n"
		;;

	esac

elif [ ${WORD_EXCLUDE_FLAG} == TRUE ] ; then

	case ${MODE} in
		OVERVIEW)
			echo -e "Overview: \n " >> ${LOG_ANALYSIS_RESULT}
			grep -n "${DEFAULT_KEYWORDS}" ${LOG_ONLY_LOCATION} | grep -v "${DEFAULT_EXCLUDED_KEYWORDS}\|${EXCLUDE_KEYWORDS}" >> ${LOG_ANALYSIS_RESULT}
			echo -e " \n    Parsed logs are stored in ${LOG_ANALYSIS_RESULT} \n"
		;;

		LINE_PARSE)
			echo "Displaying from line ${BEGIN_LINE} to ${END_LINE}"
			sed -n "${BEGIN_LINE},${END_LINE}p" ${LOG_ONLY_LOCATION} | grep -v "${EXCLUDE_KEYWORDS}" >> ${LOG_ANALYSIS_RESULT}
			echo -e " \n    Parsed logs are stored in ${LOG_ANALYSIS_RESULT} \n"
		;;

	esac

else
	CLEAN_UP
	exit 4
fi


echo "${H_BAR}" >> ${LOG_ANALYSIS_RESULT}
echo ${H_BAR} >> ${LOG_ANALYSIS_RESULT}


CLEAN_UP
#test
#test2
