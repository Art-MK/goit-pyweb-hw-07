#!/bin/bash

POSTGRES_PORT=5432
POSTGRES_USER=some_user
POSTGRES_PASSWORD=some_password

docker run --name postgres_container -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p $POSTGRES_PORT:5432 -d postgres

echo "PostgreSQL running...."
echo "Port: $POSTGRES_PORT"
echo "User: $POSTGRES_USER"
echo "Password: $POSTGRES_PASSWORD"
