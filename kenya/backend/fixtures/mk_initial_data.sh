#!/bin/bash

echo "[";

cat auth.json;
echo ","

cat email.json;
echo ","

cat message_base.json;
echo ",";

cat message_groups.json;
echo ",";

cat translated_messages.json;

echo "]";
