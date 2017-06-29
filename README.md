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

1. Install the Package Fanicontrol from AUR

2. Run the Autoconfigtool to get an Configfile 
   ```sh
   fanicontrol_autoconfig
   ```
3. Test it
   ```sh
   fanicontrol --check --config=./fanicontrol.conf
   ```   
4. If all looks fine similar to this:
```ShellSession
Config: ./fanicontrol.conf
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
 MAX TEMP    : 60
 TARGET TEMP : 45
 ALGO   : default
 TEMERATURE VARIATION: -2

Could not restore Fans !

```   
   
