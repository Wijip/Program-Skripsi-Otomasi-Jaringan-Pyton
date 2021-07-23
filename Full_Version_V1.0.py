from netmiko import ConnectHandler
import time,sys,Loading,paramiko,threading,itertools

Loading
print()
print("========================================================================================================")
print("=                                                                                                      =")
print("=                                                                                                      =")
print("=   WWW      WWW    EEEEEEEE    LLL            CCCCCCCCC     OOOOOOOO      MMM      MMM    EEEEEEEE    =")
print("=   WWW      WWW    EEE         LLL           CCCCCC         OOOOOOOO      MMMM    MMMM    EEE         =")
print("=   WWW  WW  WWW    EEEEEEE     LLL          CCCC          OOO      OOO    MMM MMMM MMM    EEEEEEE     =")
print("=   WWW WWWW WWW    EEEEEEE     LLL          CCCC          OOO      OOO    MMM  MM  MMM    EEEEEEE     =")
print("=   WWWW    WWWW    EEE         LLLLLLLLL     CCCCCCC        OOOOOOOO      MMM      MMM    EEE         =")
print("=   WWW      WWW    EEEEEEEE    LLLLLLLLL      CCCCCCCCC     OOOOOOOO      MMM      MMM    EEEEEEEE    =")
print("=                                                                                                      =")
print("=                                                                                                      =")
print("=                                                                                                      =")
print("========================================================================================================")

time.sleep(2)
dones = False
def animates():
    for d in itertools.cycle(['.','..','...','']):
        if dones:
            break
        sys.stdout.write('\rProses '+ d)
        sys.stdout.flush()
        time.sleep(0.22)
t = threading.Thread(target=animates)
t.start()

time.sleep(3)
dones = True
print()
print("======================================================================================================")
print("=                                            Catatan !!!                                             =")
print("======================================================================================================")
print("=  1. Pastikan didalam router yang akan dikonfigurasi telah terdapat konfigurasi seperti:            =")
print("=     konfigurasi DHCP Client atau IP address untuk menghubungkan program dengan                     =")
print("=     router yang akan dikonfigurasi                                                                 =")
print("=  2. Pastikan Service SSH pada router telah aktif karena program menggunakan protokol SSH           =")
print("=     untuk menerapkan konfigurasi pada router                                                       =")
print("======================================================================================================")
input("=     Press Enter to Continue"+"                                                                        =")
print("======================================================================================================")
print()
print("======================================================================================================")
print("=                                            LOGIN !!!                                               =")
print("======================================================================================================")

IP = input("Masukkan IP Address Router Anda : ")
user = input("Masukkan Username Router Anda : ")
pasw = input("Masukkan Password Router Anda : ")

RT={
    'device_type':'mikrotik_routeros',
    'ip':IP,
    'username':user,
    'password':pasw,
}

all_device = [RT]


for device in all_device:
    try:
        print(f'Connecting to {device["ip"]} ...')
        net_connect = ConnectHandler(**device)
        KS = "Koneksi Sukses ..."
        for ks in KS:
            time.sleep(0.22)
            sys.stdout.write(ks)
            sys.stdout.flush()
    except:

        print("")
        KG = "Koneksi Gagal !!! \nPeriksa IP Address, Username dan Password"
        for kg in KG:
            time.sleep(0.1)
            sys.stdout.write(kg)
            sys.stdout.flush()
        time.sleep(1)




print()
print("======================================================================================================")
print("=                                         KONFIGURASI !!!                                            =")
print("======================================================================================================")
print("1. Input Konfigurasi ")
print("2. Auto Konfig ")
print("3. Exit")
print("======================================================================================================")

while True:
    try:
        pilih = input("Pilih (input/auto/exit) : ")
    except ValueError:
        print("Sorry, I didn't understand that.")
        continue

    if pilih == 'input' or pilih == 'Input':
        break
    elif pilih == 'auto' or pilih == 'Auto':
        break
    elif pilih == 'exit' or pilih == 'Exit':
        break
    else:
        print("Sorry, Your Input Invalid")
        continue

if pilih == 'input' or pilih == 'Input':
    port ='22'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP,port,user,pasw)
    routers = [client]


    for router in routers:
        Done = False
        def animate():
            for c in itertools.cycle(['.','..','...','']):
                if Done:
                    break
                sys.stdout.write('\rProses '+c)
                sys.stdout.flush()
                time.sleep(0.22)
        t = threading.Thread(target=animate)
        t.start()
        time.sleep(3)
        Done = True
        print()
        print("===========================================================================")
        print("=                    Konfigurasi Interface Bridge                         =")
        print("===========================================================================")
        print("konfigurasi interface bridge ? ")
        while True:
            try:
                pilih = input("pilih (Yes/No) : ")
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

            if pilih == 'Yes' or pilih == 'yes':
                break
            elif pilih == 'No' or pilih == 'no':
                break
            else:
                print("Sorry, Your input invalid")
                continue

        if pilih == 'Yes' or pilih == 'yes':
            bridgename = input("Masukkan Nama Bridge Interface (tanpa spasi) : ")
            stdin, stdout, stderr = client.exec_command('interface bridge add fast-forward=no name='+bridgename)
            stdin, stdout, stderr = client.exec_command('interface bridge port add bridge='+bridgename+' interface=ether2')
            stdin, stdout, stderr = client.exec_command('interface bridge port add bridge='+bridgename+' interface=ether3')
            stdin, stdout, stderr = client.exec_command('interface bridge port add bridge='+bridgename+' interface=ether4')
            time.sleep(1)
            for line in stdout:
                print(line.strip('\n'))
            print("Interface bridge berhasil ditambahkan\n")
            time.sleep(2)
            print("===========================================================================")
            print("=                   Konfigurasi IP Address & IP POOL                      =")
            print("===========================================================================")
            ip = input("Masukkan IP Address : ")
            stdin, stdout, stderr = client.exec_command('ip address add interface='+bridgename+' address='+ip)
            for line in stdout:
                print(line.strip('\n'))
            print("IP Address berhasil di tambahkan")
            time.sleep(2)
        elif pilih == 'No' or pilih == 'no':
            print("Interface bridge tidak di terapkan ...")

            print("===========================================================================")
            print("=                   Konfigurasi IP Address & IP POOL                      =")
            print("===========================================================================")
            ip = input("Masukkan IP Adress : ")
            interface = input("Interface yang digunakan EX: ether2,ether3 : ")
            stdin, stdout, stderr = client.exec_command('ip address add interface='+interface+' address='+ip)
            for line in stdout:
                print(line.strip('\n'))
            time.sleep(2)
        print("Konfigurasi IP Pool")
        print("Ex : 192.168.1.2-192.168.1.254")
        ipool = input("Masukkan range ip pool : ")
        namepol = input("Name Pool : ")
        stdin, stdout, stderr = client.exec_command('/ip pool add name='+namepol+' ranges='+ipool)
        for line in stdout:
            print(line.strip('\n'))
        print("IP Pool berhasil Ditembahkan")
        time.sleep(2)
        print("===========================================================================")
        print("=                       Konfigurasi DHCP SERVER                           =")
        print("===========================================================================")
        ndhcp = input("nama DHCP Server : ")
        dhcppool = input("IP Pool yang digunakan : ")
        interfacedhcp = input("Interface yang digunakan : ")
        stdin,stdout, stderr = client.exec_command('/ip dhcp-server add address-pool='+dhcppool+' disabled=no interface='+interfacedhcp+' lease-time=1h name='+ndhcp)
        dhcpnet = input("Masukkan DHCP Network Ex:192.168.1.0/24 : ")
        dhcpgate = input("Masukkan DHCP Gateway Ex:192.168.1.1 : ")
        stdin, stdout, stderr = client.exec_command('/ip dhcp-server network add address='+dhcpnet+' gateway='+dhcpgate)
        for line in stdout:
            print(line.strip('\n'))
        print("DHCP Server berhasil ditambahkan ")
        time.sleep(2)
        print("===========================================================================")
        print("=                      Konfigurasi Firewall NAT                           =")
        print("===========================================================================")
        srcadd = input("Masukkan src address Ex:192.168.1.0/24 : ")
        stdin, stdout, stderr = client.exec_command('/ip firewall nat add action=masquerade chain=srcnat src-address='+srcadd)
        for line in stdout:
            print(line.strip('\n'))
        print("Firewall NAT berhasil ditambahkan")
        print("===========================================================================")
        print("=                  Konfigurasi Firewall Address list                      =")
        print("===========================================================================")

        print("=============================================================")
        print("1. Single Address list")
        print("2. Multi Address List")
        print("=============================================================")
        while True:
            try:
                pilih = input("pilih (Single/Multi) : ")
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

            if pilih == 'Single' or pilih == 'single':
                break
            elif pilih == 'Multi' or pilih == 'multi':
                break
            else:
                print("Sorry, Your input invalid")
                continue

        if pilih == 'Single' or pilih == 'single':
            ippaddlist1 = input("Masukkan IP Firewall Address List Ex:192.168.1.0/24 : ")
            nameadlist1 = input("Masukkan nama Address List : ")
            stdin,stdout,stderr = client.exec_command('/ip firewall address-list add address='+ippaddlist1+' list='+nameadlist1)
            for line in stdout:
                print(line.strip('\n'))
            print("Firewall Address List berhasil ditambahkan")
            time.sleep(2)
        elif pilih == 'Multi' or pilih == 'multi':
            ippaddlist1 = input("Masukkan IP Firewall Address List 1 Ex:192.168.1.0/24 : ")
            nameadlist1 = input("Masukkan Nama Firewall Address List 1 : ")
            ippaddlist2 = input("Masukkan IP Firewall Address List 2 Ex:192.168.2.0/24 : ")
            nameadlist2 = input("Masukkan nama Firewall Address List 2 : ")
            stdin, stdout, stderr = client.exec_command('/ip firewall address-list add address='+ippaddlist1+' list='+nameadlist1)
            stdin, stdout, stderr = client.exec_command('/ip firewall address-list add address='+ippaddlist2+' list='+nameadlist2)
            ippaddlist3 = input("Masukkan IP Firewall Address List 3 Ex:192.168.3.0.24 : ")
            nameadlist3 = input("Masukkan Nama Firewall Address List 3 :")
            stdin, stdout, stderr = client.exec_command('/ip firewall address-list add address='+ippaddlist3+' list='+nameadlist3)
            for line in stdout:
                print(line.strip('\n'))
            print("IP Firewall Address List 1 berhasil ditambahkan\n")
            time.sleep(1)
            print("IP Firewall Address List 2 berhasil ditambahkan\n")
            time.sleep(1)
            print("IP Firewall Address List 3 berhasil ditambahkan")
            time.sleep(2)
        else:
            print("Sorry, Your input invalid")


        print("===========================================================================")
        print("=                      Konfigurasi Firewall RAW                           =")
        print("===========================================================================")
        print("Masukkan Dst-Address Firewall RAW Ex: !address atau address (!lokal/lokal)")
        dstaddresslist = input("Dst-Address List : ")
        srcaddresslist = input("Src-Address List : ")
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment=Vainglory dst-address-list='+dstaddresslist+' dst-port=7000-8020 protocol=tcp src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment=Vainglory content=.superevil.net dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment="Mobile Legends" dst-address-list='+dstaddresslist+' dst-port=30000-30150 protocol=tcp src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment="Mobile Legends" content=.youngjoygame.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment="PUBG Mobile" dst-address-list='+dstaddresslist+' dst-port=10012,17500 protocol=tcp src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=fb content=.facebook.net dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=fb content=.fbcdn.net dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=twitter content=.twitter.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=twitter content=.twimg.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=tiktok content=.tiktokv.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment="PUBG Mobile" dst-address-list='+dstaddresslist+' dst-port="10491,10010,10013,10612,20002,20001,20000,12235,13748,13972,13894,11455,10096,10039" protocol=udp src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment="PUBG Mobile" content=.igamecj.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment="PUBG Mobile" content=tencentgames.helpshift.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=games address-list-timeout=none-dynamic chain=prerouting comment=Garena content=.garenanow.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=ig content=.cdninstagram.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=ig content=.instagram.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=WA content=.whatsapp.net dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=WA content=.whatsapp.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=life360 content=.life360.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        stdin,stdout,stderr = client.exec_command('/ip firewall raw add action=add-dst-to-address-list address-list=sosmed address-list-timeout=none-dynamic chain=prerouting comment=fb content=.facebook.com dst-address-list='+dstaddresslist+' src-address-list='+srcaddresslist)
        for line in stdout:
            print(line.strip('\n'))
        print("IP Firewall RAW berhasil ditambahkan")
        time.sleep(2)

        print("===========================================================================")
        print("=                      Konfigurasi Firewall Mangle                        =")
        print("===========================================================================")

        mangledstadd = input("Masukkan Mangle Dst-Address : ")
        manglesrcadd = input("Masukkan Mangle Src-Address : ")
        newconnemark = input("Masukkan nama connetion mark : ")
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting dst-address-list='+mangledstadd+' new-connection-mark='+newconnemark+' passthrough=yes src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=accept chain=prerouting connection-mark='+newconnemark+' dst-address-list='+mangledstadd+' src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting dst-address-list='+mangledstadd+' new-connection-mark=vip passthrough=yes protocol=icmp src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting comment=dns dst-address-list='+mangledstadd+' dst-port=53,5353,123,1194 new-connection-mark=vip passthrough=yes protocol=tcp src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting comment=dns dst-address-list='+mangledstadd+' dst-port=53,5353,123,1194 new-connection-mark=vip passthrough=yes protocol=udp src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=accept chain=prerouting comment=vip connection-mark=vip')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting comment=games dst-address-list=games new-connection-mark=games passthrough=yes src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=accept chain=prerouting comment=games connection-mark=games')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting comment=sosmed dst-address-list=sosmed new-connection-mark=sosmed passthrough=yes src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=accept chain=prerouting comment=sosmed connection-mark=sosmed')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=accept chain=prerouting comment=ggc-redirector connection-mark=ggc-redirector')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-connection chain=prerouting comment=all-trafik dst-address-list='+mangledstadd+' new-connection-mark=all-trafik passthrough=yes src-address-list='+manglesrcadd)
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=accept chain=prerouting comment=all-trafik connection-mark=all-trafik')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=jump chain=forward in-interface=ether1 jump-target=qos-down')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=vip-down connection-mark=vip new-packet-mark=vip-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=games-down connection-mark=games new-packet-mark=games-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=sosmed-down connection-mark=sosmed new-packet-mark=sosmed-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=browsing-down connection-bytes=0-1000000 connection-mark=all-trafik new-packet-mark=browsing-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=midle-down connection-bytes=1000001-3000000 connection-mark=all-trafik new-packet-mark=midle-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=high-down connection-bytes=3000001-1000000000 connection-mark=all-trafik new-packet-mark=high-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=unknown-down connection-mark=all-trafik new-packet-mark=unknown-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-down comment=unknown-down new-packet-mark=unknown-down passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=return chain=qos-down')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=jump chain=forward jump-target=qos-up out-interface=ether1')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=vip-up connection-mark=vip new-packet-mark=vip-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=games-up connection-mark=games new-packet-mark=games-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=sosmed-up connection-mark=sosmed new-packet-mark=sosmed-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=browsing-up connection-bytes=0-500000 connection-mark=all-trafik new-packet-mark=browsing-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=midle-up connection-bytes=501000-1500000 connection-mark=all-trafik new-packet-mark=midle-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=high-up connection-bytes=1500001-1000000000 connection-mark=all-trafik new-packet-mark=high-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=unknown-up connection-mark=all-trafik new-packet-mark=unknown-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=mark-packet chain=qos-up comment=unknown-up new-packet-mark=unknown-up passthrough=no')
        stdin,stdout,stderr = client.exec_command('/ip firewall mangle add action=return chain=qos-up')
        for line in stdout:
            print(line.strip('\n'))
        print("Firewall Mangle berhasil ditambahkan")
        time.sleep(2)
        print("===========================================================================")
        print("=                        Konfigurasi Queue Tree                           =")
        print("===========================================================================")
        download = input("Masukkan nama Parent Queue Tree download : ")
        upload = input("Masukkan nama Parent Queue Tree upload : ")
        stdin,stdout,stderr = client.exec_command('/queue tree add max-limit=3M name='+download+' parent=global queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add bucket-size=0 limit-at=64k max-limit=3M name=1.VIP packet-mark=vip-down parent='+download+' priority=1 queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add bucket-size=0 limit-at=500k max-limit=3M name=2.GAMES packet-mark=games-down parent='+download+' priority=3 queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=512k max-limit=3M name=3.NORMAL parent='+download+' queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=1M max-limit=3M name=3.2.BROWSING packet-mark=browsing-down  parent=3.NORMAL priority=5 queue=pcq-download-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=1M max-limit=3M name=3.3.MIDDLE packet-mark=midle-down parent=3.NORMAL priority=7 queue=pcq-download-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=1M max-limit=3M name=3.4.HIGH packet-mark=high-down parent=3.NORMAL queue=pcq-download-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=1M max-limit=3M name=3.5.UNKNOWN packet-mark=unknown-down parent=3.NORMAL queue=pcq-download-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add max-limit=3M name='+upload+' parent=global queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=64k max-limit=3M name=1.U-VIP packet-mark=vip-up parent='+upload+' priority=1 queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=500k max-limit=3M name=2.U-GAMES packet-mark=games-up parent='+upload+' priority=3 queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=1500k max-limit=2M name=3.U-NORMAL parent='+upload+' queue=default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=200k max-limit=2M name=3.2.U-BROWSING packet-mark=browsing-up parent=3.U-NORMAL priority=5 queue=pcq-upload-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=200k max-limit=2M name=3.3.U-MIDDLE packet-mark=midle-up parent=3.U-NORMAL priority=7 queue=pcq-upload-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=200k max-limit=2M name=3.4.U-HIGH packet-mark=high-up parent=3.U-NORMAL queue=pcq-upload-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=200k max-limit=2M name=3.5.U-UNKNOWN packet-mark=unknown-up parent=3.U-NORMAL queue=pcq-upload-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=1M max-limit=3M name=3.1.SOSMED packet-mark=sosmed-down parent=3.NORMAL priority=5 queue=pcq-download-default')
        stdin,stdout,stderr = client.exec_command('/queue tree add limit-at=200k max-limit=2M name=3.1.U-SOSMED packet-mark=sosmed-up parent=3.U-NORMAL priority=5 queue=pcq-upload-default')
        for line in stdout:
            print(line.strip('\n'))
        print("Queue Tree berhasil ditambahkan")
        time.sleep(2)
        print("===========================================================================")
        print("=                       Konfigurasi Simple Queue                          =")
        print("===========================================================================")
        simplequeue = input("Masukkan Nama Simple Queue (Tanpa Spasi) : ")
        interfacequeue = input("Interface yang digunakan : ")
        maxlimit = input("Maksimal Bandwidth UP/Down Ex:5M/5M atau 5M/3M : ")
        stdin,stdout,stderr = client.exec_command('/queue simple add max-limit='+maxlimit+' name='+simplequeue+' target='+interfacequeue)
        for line in stdout:
            print(line.strip('\n'))
        print("Simple Queue berhasil ditambahkan")
        time.sleep(2)

    print("===========================================================================")
    print("=                            CEK KONFIGURASI                              =")
    print("===========================================================================")
    input("Press Enter to Continue")
    done = False
    def animate():
        for d in itertools.cycle(['.','..','...','']):
            if done:
                break
            sys.stdout.write('\rChecking '+d)
            sys.stdout.flush()
            time.sleep(0.22)
    t=threading.Thread(target=animate)
    t.start()
    time.sleep(3)
    done = True

    print("\nCek Interface Bridege")
    time.sleep(2)
    stdin, stdout, stderr = client.exec_command('interface bridge print')
    for line in stdout:
        print(line.strip('\n'))
    stdin, stdout, stderr = client.exec_command('interface bridge port print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("\nCek IP Address")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip address print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("\nCek IP Pool")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip pool print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("\nCek DHCP-Server ")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip dhcp-server print')
    for line in stdout:
        print(line.strip('\n'))
    stdin, stdout, stderr = client.exec_command('ip dhcp-server network print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("\nCek Firewall NAT")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip firewall nat print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("\nCek Firewall Mangle")
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command('ip firewall mangle print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(2)
    input("\nPress Enter to Continue")
    print("\nCek Firewall RAW")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip firewall raw print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(2)
    input("\nPress Enter to Continue")
    print("\nCek Firewall Address List")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip firewall address-list print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("Cek Simple Queue")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('queue simple print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(3)
    print("CeK Queue Tree")
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('queue tree print')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(2)
    print("===========================================================================")
    print("=                             TEST PING !!!                               =")
    print("===========================================================================")
    done = False
    def animate():
        for p in itertools.cycle(['.','..','...','']):
            if done:
                break
            sys.stdout.write('\rping '+p)
            sys.stdout.flush()
            time.sleep(0.22)
    t=threading.Thread(target=animate)
    t.start()
    time.sleep(3)
    done = True
    print('')
    stdin, stdout, stderr = client.exec_command('ping count=5 8.8.8.8')
    for line in stdout:
        print(line.strip('\n'))
    stdin, stdout, stderr = client.exec_command('ping count=5 google.com')
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(2)
    input("\nPress Enter to Continue")
    print("===========================================================================")
    print("=                          EXPORT KONFIGURASI                             =")
    print("===========================================================================")
    print("export file konfigurasi ")
    nameexport = input("Nama File export : ")
    done = False
    def animate():
        for d in itertools.cycle(['.','..','...','']):
            if done:
                break
            sys.stdout.write("\rExporting "+d)
            sys.stdout.flush()
            time.sleep(0.22)
    t=threading.Thread(target=animate)
    t.start()
    time.sleep(3)
    done = True
    stdin, stdout, stderr = client.exec_command("export file="+nameexport)
    for line in stdout:
        print(line.strip('\n'))
    time.sleep(2)
    exs = "\nExport Sukses ...\nKonfigurasi Dan Cek Konfigurasi Selesai"
    for ex in exs:
        time.sleep(0.1)
        sys.stdout.write(ex)
        sys.stdout.flush()


    time.sleep(1)
    EX = "\nHave Nice Day\nBye Bye ..."
    for ex in EX:
        time.sleep(0.1)
        sys.stdout.write(ex)
        sys.stdout.flush()
    time.sleep(2)
    client.close()
    exit()
elif pilih == 'auto' or pilih == 'Auto':
    done = False
    def animate():
        for d in itertools.cycle(['.','..','...','']):
            if done:
                break
            sys.stdout.write("\rProses "+d)
            sys.stdout.flush()
            time.sleep(0.22)
    d=threading.Thread(target=animate)
    d.start()
    time.sleep(3)
    done = True

    with open("bridge") as brg:
        bridge = brg.read().splitlines()
    with open("ip add") as ipad:
        ipaddress = ipad.read().splitlines()
    with open("ip pool") as pool:
        ippool = pool.read().splitlines()
    with open("dhcp-server") as dhcp:
        DHCP = dhcp.read().splitlines()
    with open("Firewall-NAT") as nat:
        NAT = nat.read().splitlines()
    with open("Firewall-Add-List") as addlist:
        addresslist = addlist.read().splitlines()
    with open("Firewall-RAW") as RAW:
        fireRAW = RAW.read().splitlines()
    with open("Firewall-Mangle") as Mangle:
        FireMangle = Mangle.read().splitlines()
    with open("Queue-Tree") as Tree:
        QueTree = Tree.read().splitlines()
    with open("Simple-Queue") as Simple:
        QueSimple = Simple.read().splitlines()
    time.sleep(2)
    print('\n')
    print("Please Wait ...")
    time.sleep(2)
    print('\n')
    done = False
    def animate():
        for co in itertools.cycle(['.','..','...','']):
            if done:
                break
            sys.stdout.write("\rconfiguration "+co)
            sys.stdout.flush()
            time.sleep(0.22)
    co=threading.Thread(target=animate)
    co.start()
    time.sleep(3)
    done = True

    net_connect = ConnectHandler(**device)
    #config Interface bridge
    print("\n===========================================================================")
    print("=                    Konfigurasi Interface Bridge                         =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(bridge)
    print(f'\nInterface Bridge berhasil ditambahkan')

    #config IP Address
    print("\n===========================================================================")
    print("=                   Konfigurasi IP Address & IP POOL                      =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(ipaddress)
    print(f'\nIP Address berhasil ditambahkan')

    #config IP Pool
    time.sleep(1)
    output = net_connect.send_config_set(ippool)
    print(f'\nIP Pool berhasil ditambahkan')

    #config DHCP Server
    print("\n===========================================================================")
    print("=                       Konfigurasi DHCP SERVER                           =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(DHCP)
    print(f'\nDHCP-Server berhasil ditambahkan')

    #config Firewall NAT
    print("\n===========================================================================")
    print("=                      Konfigurasi Firewall NAT                           =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(NAT)
    print(f'\nFirewall NAT berhasil ditambahkan')

    #config Firewall Address-list
    print("\n===========================================================================")
    print("=                  Konfigurasi Firewall Address list                      =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(addresslist)
    print(f'\nFirewall Address-list berhasil ditambahkan')

    #config Firewall RAW
    print("\n===========================================================================")
    print("=                      Konfigurasi Firewall RAW                           =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(fireRAW)
    print(f'\nFirewall RAW berhasil ditambahkan')

    #config Firewall Mangle
    print("\n===========================================================================")
    print("=                      Konfigurasi Firewall Mangle                        =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(FireMangle)
    print(f'\nFirewall Mangle berhasil ditambahkan')

    #config Queue Tree
    print("\n===========================================================================")
    print("=                        Konfigurasi Queue Tree                           =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(QueTree)
    print(f'\nQueue Tree berhasil ditambahkan')

    #config Simple Queue
    print("\n===========================================================================")
    print("=                       Konfigurasi Simple Queue                          =")
    print("===========================================================================")
    time.sleep(1)
    output = net_connect.send_config_set(QueSimple)
    print(f'\nSimple Queue berhasil ditambahkan')

    port ='22'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP,port,user,pasw)
    routers = [client]

    for router in routers:
        print("===========================================================================")
        print("=                            CEK KONFIGURASI                              =")
        print("===========================================================================")
        input("Press Enter to Continue")
        done = False
        def animate():
            for d in itertools.cycle(['.','..','...','']):
                if done:
                    break
                sys.stdout.write('\rChecking '+d)
                sys.stdout.flush()
                time.sleep(0.1)
        t=threading.Thread(target=animate)
        t.start()
        time.sleep(3)
        done = True

        print("\nCek Interface Bridge")
        time.sleep(2)
        stdin, stdout, stderr = client.exec_command('interface bridge print')
        for line in stdout:
            print(line.strip('\n'))
        stdin, stdout, stderr = client.exec_command('interface bridge port print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("\nCek IP Address")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('ip address print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("\nCek IP Pool")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('ip pool print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("\nCek DHCP-Server ")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('ip dhcp-server print')
        for line in stdout:
            print(line.strip('\n'))
        stdin, stdout, stderr = client.exec_command('ip dhcp-server network print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("\nCek Firewall NAT")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('ip firewall nat print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("\nCek Firewall Mangle")
        time.sleep(3)
        stdin, stdout, stderr = client.exec_command('ip firewall mangle print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(2)
        input("\nPress Enter to Continue")
        print("\nCek Firewall RAW")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('ip firewall raw print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(2)
        input("\nPress Enter to Continue")
        print("\nCek Firewall Address List")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('ip firewall address-list print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("Cek Simple Queue")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('queue simple print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(3)
        print("CeK Queue Tree")
        time.sleep(1)
        stdin, stdout, stderr = client.exec_command('queue tree print')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(2)
        print("===========================================================================")
        print("=                             TEST PING !!!                               =")
        print("===========================================================================")
        done = False
        def animate():
            for p in itertools.cycle(['.','..','...','']):
                if done:
                    break
                sys.stdout.write('\rping '+p)
                sys.stdout.flush()
                time.sleep(0.22)
        t=threading.Thread(target=animate)
        t.start()
        time.sleep(3)
        done = True
        print('\n')
        stdin, stdout, stderr = client.exec_command('ping count=5 8.8.8.8')
        for line in stdout:
            print(line.strip('\n'))
        stdin, stdout, stderr = client.exec_command('ping count=5 google.com')
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(2)
        input("\nPress Enter to Continue")
        print("===========================================================================")
        print("=                          EXPORT KONFIGURASI                             =")
        print("===========================================================================")
        time.sleep(1)
        print("export file konfigurasi : ")
        nameexport = input("Nama File export : ")
        done = False
        def animate():
            for d in itertools.cycle(['','.','..','...','']):
                if done:
                    break
                sys.stdout.write("\rExporting "+d)
                sys.stdout.flush()
                time.sleep(0.10)
        t=threading.Thread(target=animate)
        t.start()
        time.sleep(3)
        done = True
        stdin, stdout, stderr = client.exec_command("export file="+nameexport)
        for line in stdout:
            print(line.strip('\n'))
        time.sleep(2)
        exs = "\nExport Sukses ...\nKonfigurasi Dan Cek Konfigurasi Selesai"
        for ex in exs:
            time.sleep(0.1)
            sys.stdout.write(ex)
            sys.stdout.flush()

        time.sleep(1)
        EX = "\nHave Nice Day\nBye Bye ..."
        for ex in EX:
            time.sleep(0.1)
            sys.stdout.write(ex)
            sys.stdout.flush()
        time.sleep(2)
        client.close()
        exit()
elif pilih == 'exit' or pilih == 'Exit':
    EX = "Have Nice Day\nBye Bye ..."
    for ex in EX:
        time.sleep(0.1)
        sys.stdout.write(ex)
        sys.stdout.flush()
    time.sleep(1)
    exit()
