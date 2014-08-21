#!/bin/bash
echo -n  "The time and date are: "
date
echo "Let's see who's logged into the system:"
who
echo "User info for userid: $USER"
echo UID: ${UID}
echo "HOME: ${HOME}"
