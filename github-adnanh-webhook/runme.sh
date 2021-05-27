#!/bin/bash
sudo apt install webhook
webhook --hooks hooks.json -hotreload -port 9099 -verbose
