SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid inline bash code" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-001.yaml 2>&1 | grep -e '\(Processing\|Exit code\|hello\)'"
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-11]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "print out hello world" ]
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "| hello world 1!" ]
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]

    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| hello world 2!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}