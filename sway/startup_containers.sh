#!/bin/bash
delay="0.1"
if ! pgrep -x "thunar" > /dev/null; then
    thunar & disown
    sleep $delay
    thunar & disown
    sleep $delay
    foot & disown
    sleep $delay
    ulauncher-toggle
    ulauncher-toggle
    sleep 2
    swaymsg move down
    swaymsg focus up
    swaymsg focus left
    swaymsg move right
    swaymsg move right
    swaymsg rename workspace to 9
    swaymsg move workspace to output eDP-1
fi
