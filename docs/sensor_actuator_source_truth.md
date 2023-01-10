# Sensor and Actuator Source of Truth

| Location         | Device ID | Device Type                  | Friendly Name                          | Possible States                                                                                 |
| ---------------- |-----------| ---------------------------- |----------------------------------------| ----------------------------------------------------------------------------------------------- |
| Air Loop         | c0        | SHT40                        | Shared Temp Humidity Sensor            | -                                                                                               |
| Air Loop         | c1        | SCD41                        | Shared CO2 Temp Humidity Sensor        | -                                                                                               |
| Air Loop         | c2        | IPC10100                     | Shared Temp Pressure Sensor            | -                                                                                               |
| Air Loop         | c7        | YFS201                       | Shared Flow Rate Sensor                | -                                                                                               |
| Air Loop         | c8        | SEN0441                      | Shared H2 Sensor                       | -                                                                                               |
| Air Loop         | c9        | SEN0321                      | Shared Ozone Sensor Near Generator     | -                                                                                               |
| Air Loop         | ca        | SEN0321                      | Shared Ozone Sensor Sensor Loop        | -                                                                                               |
| Air Loop         | e0        | Rotary Diverter Valve 1>6    | Rotary Diverter Valve From Air Loop    | 0 to compost loop<br />1 shredder storage<br />2 bioreactor 1<br />3 bioreactor 2<br />4 bsf reproduction<br />5 sieve   |
| Air Loop         | e1        | Rotary Diverter Valve 6>1    | Rotary Diverter Valve To Air Loop      | 0 from compost loop<br />1 shredder storage<br />2 bioreactor 1<br />3 bioreactor 2<br />4 bsf reproduction<br />5 sieve |
| Air Loop         | e7        | Flap Diverter Valve          | Flap Diverter Valve Sensor Loop Bypass | 0 default<br />1 bypass                                                                              |
| Air Loop         | e8        | Flap Diverter Valve          | Flap Diverter Valve Radiator Bypass    | 0 default<br />1 bypass                                                                              |
| Air Loop         | ea        | Flap Diverter Valve          | Flap Diverter Valve Sensor Box Bypass  | 0 default<br />1 bypass                                                                              |
| Air Loop         | eb        | Discrete Flap Diverter Valve | Environment Exchange Out               | 0 0% air to env<br />1 5% (ish)<br />...<br />19 100%                                                          |
| Air Loop         | ec        | Discrete Flap Diverter Valve | Environment Exchange In                | 0 0% air from env<br />1 5% (ish)<br />...<br />19 100%                                                        |
| Air Loop         | f1        | Air Mover                    | Regen Blower                           | 0 off<br />1 on                                                                                      |
| Air Loop         | f4        | UVC Light                    | UVC Light                              | 0 off<br />1 on                                                                                      |
| Air Loop         | f3        | Ozone Generator              | Ozone Generator                        | 0 off<br />1 on                                                                                      |
| Compost Loop     | e2        | Rotary Diverter Valve 1>6    | Rotary Diverter Valve Compost Loop     | 0 to air loop<br />1 -<br />2 bioreactor 1<br />3 bioreactor 2<br />4 bsf reproduction<br />5 sieve                      |
| Shredder Storage | c3        | DS18B20                      | Soil Temp Probe Shredder Storage       | -                                                                                               |
| Shredder Storage | e3        | Butterfly Valve              | Butterfly Valve From Shredder Storage  | 0 off<br />1 on                                                                                      |
| Shredder Storage | ed        | Air Hammer Valve             | Air Hammer Shredder Storage            | 0 off<br />1 on                                                                                      |
| Shredder Storage | f5        | Heater Relay                 | Heater Relay Shredder Storage          | 0 off<br />1 on                                                                                      |
| Shredder Storage | f6        | Water Pump Relay             | Water Pump Relay Shredder Storage      | 0 off<br />1 on                                                                                      |
| Bioreactor1      | c4        | DS18B20                      | Soil Temp Probe Bioreactor1            | -                                                                                               |
| Bioreactor1      | e4        | Butterfly Valve              | Butterfly Valve From Bioreactor1       | 0 off<br />1 on                                                                                      |
| Bioreactor1      | ee        | Air Hammer Valve             | Air Hammer Bioreactor1                 | 0 off<br />1 on                                                                                      |
| Bioreactor1      | f7        | Heater Relay                 | Heater Relay Bioreactor1               | 0 off<br />1 on                                                                                      |
| Bioreactor1      | f8        | Water Pump Relay             | Water Pump Relay Bioreactor1           | 0 off<br />1 on                                                                                      |
| Bioreactor2      | c5        | DS18B20                      | Soil Temp Probe Bioreactor2            | -                                                                                               |
| Bioreactor2      | e5        | Butterfly Valve              | Butterfly Valve From Bioreactor2       | 0 off<br />1 on                                                                                      |
| Bioreactor2      | ef        | Air Hammer Valve             | Air Hammer Bioreactor2                 | 0 off<br />1 on                                                                                      |
| Bioreactor2      | f9        | Heater Relay                 | Heater Relay Bioreactor2               | 0 off<br />1 on                                                                                      |
| Bioreactor2      | fa        | Water Pump Relay             | Water Pump Relay Bioreactor2           | 0 off<br />1 on                                                                                      |
| BSF Reproduction | c6        | DS18B20                      | Soil Temp Probe BSFReproduction        | -                                                                                               |
| BSF Reproduction | e6        | Butterfly Valve              | Butterfly Valve From BSFReproduction   | 0 off<br />1 on                                                                                      |
| BSF Reproduction | f0        | Air Hammer Valve             | Air Hammer BSFReproduction             | 0 off<br />1 on                                                                                      |
| BSF Reproduction | f2        | BSF Light                    | BSFReproduction Light                  | 0 off<br />1 on                                                                                      |
| BSF Reproduction | fb        | Heater Relay                 | Heater Relay BSFReproduction           | 0 off<br />1 on                                                                                      |
| BSF Reproduction | e9        | Water Pump Relay             | Water Pump Relay BSFReproduction       | 0 off<br />1 on                                                                                      |

![Simplified System Diagram](./resources/simplified_system_diagram.drawio?raw=true)

<br>
