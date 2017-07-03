# fanicontrol

**__This Software is Alpha don´ cry about burned mainboards...__**

A new way controlling your Fans under Linux ...


**The Problems**

The most common way to control a fan is to get a related temperature and to calculate a fan speed.
Example : 35 C° -> 35 * 100 = 3500 rpm . Then we raise or lower the pwm Value until we've got 3500 rpm.
This approach is very simple but also stupid. Because we didn't know if this fanspeed is too high and you are annoyed by the noise of your fan or the fanspeed is so low that your temperature still raise ...

A often seen Problem under Linux is that the Fanspeed is missing if you want to control the fanspeed by yourself. It seems a good way for Hardware manufactures to avoid People from controlling fans...

**The Solution**

... in progress

***Quickstart for Arch Users***

1. Install the package fanicontrol from AUR

2. Run the autoconfigtool to get an configfile 
   ```sh
   fanicontrol_autoconfig
   ```
3. Test it
   ```sh
   fanictl --check --config=./fanicontrol.conf
   ```   
4. If all looks fine similar to this:
```ShellSession
Config: ./fanicontrol.conf

[global]
interval = 1
pinterval = 5
logpath = /tmp/fanilog
file_loglevel = None
cli_loglevel = WARNING
rotateLog = h

[fan_asus]
fan_name = pwm1
device_name = asus
sensor_list = sensor_asus0,sensor_coretemp0,sensor_coretemp1,sensor_coretemp2,sensor_acpitz0,sensor_pch_wildcat_point0,
minPWM = 30
startPWM = 30
algo = default
lock = 5
method= relative

[sensor_asus0]
device_name = asus
sensor_name = temp1_input
target_temp = 45
max_temp = 60
algo = default
method = relative

[sensor_coretemp0]
device_name = coretemp
sensor_name = temp2_input
target_temp = 45
max_temp = 60
algo = default
method = relative

[sensor_coretemp1]
device_name = coretemp
sensor_name = temp3_input
target_temp = 45
max_temp = 60
algo = default
method = relative

[sensor_coretemp2]
device_name = coretemp
sensor_name = temp1_input
target_temp = 45
max_temp = 60
algo = default
method = relative

[sensor_acpitz0]
device_name = acpitz
sensor_name = temp1_input
target_temp = 45
max_temp = 60
algo = default
method = relative

[sensor_pch_wildcat_point0]
device_name = pch_wildcat_point
sensor_name = temp1_input
target_temp = 45
max_temp = 60
algo = default
method = relative


Could not restore Fans !

```   
5. copy conf
   ```sh
   sudo cp .fanicontrol.conf /etc/fanicontrol.conf
   ```   
6. enable service
   ```sh
   sudo systemctl enable fanicontrol.service
   ```   
7. start service
   ```sh
   sudo systemctl start fanicontrol.service
   ```   
8. keep watching temps (needs the lmsensor package) :
   ```sh
   watch -n 5 senors
   ```   
9. modify your config to your needs

10. be happy and if you want to write me an mail : dev_tsonntig@tuta.io



