---
title: Vagrant FreeBSD Appliance Box - Part 1
date: 2015-03-25
slug: vagrant-freebsd-p1
author: Eric Gustafson
tags: [Vagrant, FreeBSD]
---

A Vagrant 'network appliance' based on FreeBSD.

> *Author's note: This posting was rushed in an attempt to capture the knowledge
> gathered thus far in my learning process.  The posting is a bit of a work in
> progress - expect updates over the next few weeks as the process is refined.*

This is part 1, (and take, 1 I suspect), describing the creation of a Vagrant Box
intended to be used as a firewall / router appliance with Vagrant.  I have
reached the limits of VirtualBox with respect to networking and the solution is
to stop using VirtualBox's built in networking and build an appliance that
provides the needed functionality.  This "appliance" will sit between a
host-only network, where the rest of any development project will sit, and "the
outside".  The outside can be accessed through either NAT or Bridged networking
with the pseudo-default NAT adapter configured as the first adapter in Vagrant.

This appliance "box" should be an evolving project.  The first step is to create
a VirtualBox image, along with Vagrant control files, package it as a "Vagrant
Box", and publish it on HashiCorp's Atlas repository -- possibly other
locations as well.  Subsequent steps will elaborate configuration of the network
functions through a Vagrantfile, or ancillary configuration file.

The initial network functionality that this project will be seeking to provide
is:

- IPv6 Support -- not easily controlled through VirtualBox/Vagrant.
- DHCP Configuration, both v4 and DHCPv6.
- DNS Service, again with IPv6 and v4 support.
- Configurable IPv6 Tunneling for public v6 connectivity.
- Configurable IPv4 NAT for public v4 connectivity.

# Creating a FreeBSD Vagrant Box

The process I followed started like many of the other articles written about how
to create [Vagrant Base Boxes][box].  See the [References]({{< relref
"#references" >}}) section at the end of this article for links to other
postings I pulled inspiration from.

[box]: https://docs.vagrantup.com/v2/boxes/base.html

The primary difference, in my mind, between building a generic Vagrant Base Box
and an "appliance" box is that resources and host configuration should be
specialized for the purpose and not generalized for flexibility.  To that end,
my choices of configuration are aimed at minimum resource utilization and
specific configuration for the purpose.  It should be noted that, just like
other Vagrant box definitions, this one can be modified to suit individual
purposes as well.

|              |                                         |
|--------------|-----------------------------------------|
| Box Name:    | freebsd-10.1-amd64-gateway              |
| Type:        | BSD / FreeBSD                           |
| Memory:      | 384 MB                                  |
| CPU:         | 1                                       |
| Disk:        | 4G (dynamic VMDK)                       |
| Network 1:   | NAT (para-virtualized controller)       |
| Port Forward:| - Name: SSH <br/> - Protocol: TCP <br/> - Host Port: 2222 </br> - Guest Port: 22 |


## Install FreeBSD onto a VirtualBox host:

The image was created by installing FreeBSD 10.1 from the ISO image taking the
following steps:

- Hostname: gw
- No optional components installed
- Partitions: (no swap)
  - freebsd-boot: 512k
  - freebsd-root(UFS): remainder
- Root password: 'vagrant'
- Timezone: UTC
- Services started at boot:  sshd, ntpd
- User: 'vagrant' w/ password 'vagrant', shell: csh, group 'vagrant' + 'wheel'

## Reboot and Configure the VM

Log in as root and update the system:

```bash
$ freebsd-update fetch
$ freebsd-update install
$ pkg update
$ pkg upgrade
```

Install `sudo` and `bash`; configure the `vagrant` user to have sudo access with out
entering a password:

```bash
$ pkg install bash
# follow the instructions regarding `fdesc`
$ mount -t fdescfs fdesc /dev/fd
$ echo "fdesc  /dev/fd  fdescfs   rw  0  0" >> /etc/fstab
#
$ pkg install sudo
$ echo "vagrant ALL=(ALL) NOPASSWD:ALL" > /usr/local/etc/sudoers.d/vagrant
```

Log out and log back in as user `vagrant`.  Configure SSH access for user
`vagrant` using the Vagrant public keys:

```bash
$ sudo pkg install wget
$ mkdir -p ~/.ssh
$ wget --no-check-certificate \
       https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub \
       -O ~/.ssh/authorized_keys
$ chmod 0700 ~/.ssh
$ chmod 0400 ~/.ssh/authorized_keys
```

Ensure the the following are set in the `/etc/ssh/sshd_config` file:

```
Port  22
PubkeyAuthentication  yes
AuthorizedKeysFile  %h/.ssh/authorized_keys
PermitEmptyPasswords  no
```

Add additional packages.  These packages are required to make the host into an
appliance, or are utilitarian in nature:

```bash
# Required
$ sudo pkg install dnsmasq
$ sudo pkg install python
# Utilities
$ sudo pkg install bind-tools
$ sudo pkg install curl
```

Shutdown the VM in preparation for packaging:

```
$ sudo shutdown -p now
```

## Package the Box

From the VirtualBox host machine:

```bash
$ vagrant package --base freebsd-10.1-amd64-gateway
```

Note that the VirtualBox VM name is "freebsd-10.1-amd64-gateway".

# References

Building Vagrant Boxen
: http://williamwalker.me/blog/creating-a-custom-vagrant-box.html
: https://blog.engineyard.com/2014/building-a-vagrant-box
: http://www.skoblenick.com/vagrant/creating-a-custom-box-from-scratch/

Previous Articles on IPv6
: [IPv6 Tunneling over IPv4 Networks]({{< ref "post/2015-02-25-ipv6-tunneling.md" >}})
: [IPv6 Network (Auto) Configuration]({{< ref "post/2015-03-06-ipv6-dhcpv6.md" >}})

<!--
Local Variables:
fill-column: 80
End:
-->
