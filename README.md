# fanicontrol

**__This Software is Alpha don´ cry about burned mainboards...__**

A new way controlling your Fans under Linux ...


**The Problems**

The most common way to control a fan is to get a related temperature and to calculate a fan speed.
Example : 35 C° -> 35 * 100 = 3500 rpm . Then we raise or lower the pwm Value until we've got 3500 rpm.
This approach is very simple but also stupid. Because we didn't know if this fanspeed is too high and you are annoyed by the noise of your fan or the fanspeed is so low that your temperature still raise ...

A often seen Problem under Linux is that the Fanspeed is missing if you want to control the fanspeed by yourself. It seems a good way for Hardware manufactures to avoid People from controlling fans...

**The Solution**

...

***Quickstart***

1. clone the repo 

```ShellSession
git clone "https://github.com/tsonntig/Fanicontrol.git"
Klone nach 'Fanicontrol' ...
remote: Counting objects: 47, done.
remote: Compressing objects: 100% (39/39), done.
remote: Total 47 (delta 19), reused 20 (delta 6), pack-reused 0
Entpacke Objekte: 100% (47/47), Fertig.
```
2. let autoconfig do his work

```ShellSession
$ ./Fanicontrol/src/autoconfig 
Start Autoconfig, please check the generated Configfile !
Writing to :/home/user/fanicontrol.conf
Search for Sensors
Search for Fans
success !
 Please check your config with fanicontrol --check!
```
3. test the generated config

```ShellSession
$ ./Fanicontrol/src/fanicontrol --check -c ./fanicontrol.conf
Config: ./fanicontrol.conf
06-26 03:01:49 | INFO | create_logger | 3.6.1 (default, Mar 27 2017, 00:27:06) 
[GCC 6.3.1 20170306]
**** FANS ****

 NAME        : fan_asus
 PWM PATH    : /sys/devices/platform/asus-nb-wmi/hwmon/hwmon3/pwm1
 MIN PWM     : 30
 START PWM   : 30
 ENABLE PATH : /sys/devices/platform/asus-nb-wmi/hwmon/hwmon3/pwm1_enable
 SENSORS: 
 		sensor_0_asus
 		sensor_1_coretemp
 		sensor_2_coretemp
 		sensor_3_coretemp
 		sensor_4_acpitz
 		sensor_5_pch_wildcat_point

**** SENSORS ****

 NAME        : sensor_0_asus
 SENSOR PATH     : /sys/devices/platform/asus-nb-wmi/hwmon/hwmon3/temp1_input
 MAX TEMP    : 50
 TARGET TEMP : 40
 ALGO   : default
 TEMERATURE VARIATION: 0

Could not restore Fans !
$ 

```
