#!/bin/bash
flake8 antiddosclient | tee flake8.log
exit ${PIPESTATUS[0]}
