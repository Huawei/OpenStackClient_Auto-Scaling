#!/bin/bash
flake8 asclient | tee flake8.log
exit ${PIPESTATUS[0]}
