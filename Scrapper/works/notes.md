https://www.conduktor.io/kafka/kafka-topics-cli-tutorial/

# on BROKER server to test producer / consumer

kafka-console-producer --topic mytopic --bootstrap-server broker:9092
kafka-console-consumer --topic mytopic --bootstrap-server broker:9092

# powershell test port accessible

Test-NetConnection -ComputerName "localhost" -Port 9092

9021 (control-center)


# if permission denied windows for volumes:
cd /mnt/wsl/docker-desktop-data/version-pack-data/community/docker/volumes/
or
cd /mnt/wsl/docker-desktop-data/data/docker/volumes
sudo chmod -R 777 .

if bad mounted:
sudo mount -t ext4 /dev/sde /mnt/wsl/docker-desktop-data