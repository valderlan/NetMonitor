
<!------------------------------------------------------------------------------------------------->
# Introdução
<!------------------------------------------------------------------------------------------------->

Este projeto trata da captura do fluxo de pacotes por meio de uma interface de rede, salva cada fragmento de tamanho específico em um arquivo PCAP e, em seguida, converte-o automaticamente no arquivo CSV extraído do recurso pelo CICFlowMeter-4.0.
Este projeto foi clonado da [fonte (source)](https://github.com/iPAS/TCPDUMP_and_CICFlowMeter), onde foram feitas modificações para o seu adaquado na minha aplicação. 


Ferramentas utilizadas aqui são __TCPdump__ e [CICFlowMeter](https://www.unb.ca/cic/research/applications.html#CICFlowMeter) 

<!------------------------------------------------------------------------------------------------->
# Uso
<!------------------------------------------------------------------------------------------------->

## Para Executar

Chamar __capture_interface_pcap.sh__ irá capturar os pacotes desde o início até um horário específico no script, periodicamente. 
Cada vez que o arquivo PCAP é salvo, o script __convert_pcap_csv.sh__ será chamado de conversor, __CICFlowMeter__.

```bash
capture_interface_pcap.sh <interface> <pcap_output_dir> [priviledged_user_name]
```

Por exemplo:

```bash
capture_interface_pcap.sh wlan0 pcap
```

ou

```bash
capture_interface_pcap.sh eth0 output_dir bobuser
```


## To Run on Startup

Edit the working directory in file __pcap2ciclog.service__, and also
    the executed script shoud be refered with absolute path:

```
...
[Service]
WorkingDirectory=/home/../../TCPDUMP_and_CICFlowMeter
ExecStart=/home/../../TCPDUMP_and_CICFlowMeter/pcap2ciclog.sh
...

```

Then, link it into the directory __/lib/systemd/system__:

```bash
cd /lib/systemd/system
sudo ln -sf <the-dir>/pcap2ciclog.service
```

Enable the service:

```bash
sudo systemctl enable pcap2ciclog.service
```

Finally, let's get started!

```bash
sudo systemctl start pcap2ciclog.service
```


<!------------------------------------------------------------------------------------------------->
# Note on Issues
<!------------------------------------------------------------------------------------------------->

## To Fix the _Permission Denied_ Problem

In some case of using on Ubuntu with __Apparmor__, you may has a 'permission denied' issue
    when __tcpdump__ tries to execute a script.
    It is a security measure. To relax, please add the following line into file
    __/etc/apparmor.d/usr.sbin.tcpdump__:

```
/usr/sbin/tcpdump {
  ...
  # for -z
  /**/* ixr,      # <-- add me!
  ...
}
```

Then, restart the service:

```bash
sudo service apparmor restart
```


## To Fix _java.lang.UnsatisfiedLinkError_ Problem

Due to the libpcap-dev package was not installed.
The error will be shown:

    Exception in thread "main" java.lang.UnsatisfiedLinkError: com.slytechs.library.NativeLibrary.dlopen(Ljava/lang/String;)J
            at com.slytechs.library.NativeLibrary.dlopen(Native Method)
            at com.slytechs.library.NativeLibrary.<init>(Unknown Source)
            at com.slytechs.library.JNILibrary.<init>(Unknown Source)
            at com.slytechs.library.JNILibrary.loadLibrary(Unknown Source)
            at com.slytechs.library.JNILibrary.register(Unknown Source)
            at com.slytechs.library.JNILibrary.register(Unknown Source)
            at com.slytechs.library.JNILibrary.register(Unknown Source)
            at org.jnetpcap.Pcap.<clinit>(Unknown Source)
            at cic.cs.unb.ca.jnetpcap.PacketReader.config(PacketReader.java:58)
            at cic.cs.unb.ca.jnetpcap.PacketReader.<init>(PacketReader.java:52)
            at cic.cs.unb.ca.ifm.CICFlowMeter.main(CICFlowMeter.java:93)

Please install via:

```bash
sudo apt install libpcap-dev
```

For furture OSs, please follow the guildline on https://javatutorial.net/capture-network-packages-java.


## To Build CICFlowMeter Command-line Version

The forked and revised version of ISCX/CICFlowMeter can be found at https://github.com/iPAS/CICFlowMeter.
Nevertheless, in case you need to know how to make it by yourself,
    or if the next version need the maintenance again,
    the guidance is directed by the following clues.

### Get CICFlowMeter

```bash
git clone https://github.com/ISCX/CICFlowMeter.git
```

Then, go inside.

### Get Gradle (option)

```bash
chmod +x gradlew
./gradlew
```

However, this is not neccessary in case you already have it.

### Update CICFlowMeter

In CICFlowMeter directory, please:

```bash
git fetch --all
git reset original/master --hard
```

All code will be renew as the original repository.
All revised files will be gone, even yours.

### Build CICFlowMeter

* Edit the build.gradle file, enable to find JNetPCAP package:

    1. Add a new repository:

        ```
        repositories {
            ...

            maven {
                url "http://clojars.org/repo/"
            }

        }
        ```

    2. Reversion the dependency:

        ```
        dependencies {
            ...

            // compile group: 'org.jnetpcap', name: 'jnetpcap', version:'1.4.1'
            compile group: 'jnetpcap', name: 'jnetpcap', version: '1.4.r1425-1g'

        ```

* To make the command-line enable:

    1. Change all occurences of the following:

            cic.cs.unb.ca.ifm.App

        to

            cic.cs.unb.ca.ifm.CICFlowMeter

    2. Exclude the GUI besides include the command-line source file:

        ```
        sourceSets {
            main {
                java {
                    srcDir 'src'
                    // exclude '**/CICFlowMeter.java'
                    exclude '**/App.java'
                }
            }
        }
        ```

    3. Edit the code __src/main/java/cic/cs/unb/ca/ifm/CICFlowMeter.java__ by looking at
        [my CICFlowMeter.java](
        https://github.com/iPAS/CICFlowMeter/blob/command-line/src/main/java/cic/cs/unb/ca/ifm/CICFlowMeter.java).

* Then, build the project:

    ```bash
    gradle build
    ```

### Test Running CICFlowMeter

* To run via Gradle:

    ```bash
    gradle run
    ```

    The result might be shown like the following:

        type Jar
        type JavaExec
        :compileJava UP-TO-DATE
        :processResources UP-TO-DATE
        :classes UP-TO-DATE
        :run
        cic.cs.unb.ca.ifm.CICFlowMeter Sorry,no pcap files can be found under: <...some path...>

        BUILD SUCCESSFUL

        Total time: 0.936 secs

### Install

The built package is in directory __CICFlowMeter_repo/build/distributions/__.
Get and place in a directory that fit.

### Update the Runner Script

After the distribution package was gotten,
    unpack and revise the code in script __CICFlowMeter-3.0/bin/CICFlowMeter__:

1. Change the reference to libraries with real path:

        DEFAULT_JVM_OPTS='"-Djava.library.path=../lib/native"'

    to

        DEFAULT_JVM_OPTS='"-Djava.library.path='$APP_HOME/lib/native'"'

2. Call to command-line instead of GUI application:

        eval set -- $DEFAULT_JVM_OPTS $JAVA_OPTS $CIC_FLOW_METER_OPTS -classpath "\"$CLASSPATH\"" cic.cs.unb.ca.ifm.App "$APP_ARGS"

    to

        eval set -- $DEFAULT_JVM_OPTS $JAVA_OPTS $CIC_FLOW_METER_OPTS -classpath "\"$CLASSPATH\"" cic.cs.unb.ca.ifm.CICFlowMeter "$APP_ARGS"


## To Build CICFlowMeter-4

- __gradle__ and __maven__ are required

# NetMonitor
