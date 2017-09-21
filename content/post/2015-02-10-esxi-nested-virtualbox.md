---
title:   Nested Virtualization - VirtualBox inside ESXi
date:    2015-02-10
slug:    esxi-nested-virtualbox
author:  Eric Gustafson
tags:    [virtualization, VirtualBox, VMWare]
---

This process describes how to configure an ESXi Linux guest so that the guest
can then run VirtualBox and create a nested, 64 bit guest within the ESXi guest
-- Nested Virtualization.

There is nothing special about the use of Linux as either the ESXi guest, or the
nested guest.  Any supported operating system *should* work at either nesting
level.  This includes nesting ESXi inside of ESXi, which appears to be the most
common form of documentation to describe this process.

This process details *manually* editing an ESXi hosts's VM configuration file to
direct the inclusion of support for virtualization from within the guest.  ESXi
version 5.5 is specifically addressed.  I found a number of blog postings
detailing earlier versions of ESXi, unfortunately the process changed in 5.5 and
the newer version is much less prevalently documented.  I also found blog
postings detailing how to use the vSphere Web UI to effect the reconfiguration.
Unfortunately, the Web UI is not part of the free license VMWare grants for an
ESXi host.  As a consequence, this posting details the manual editing to enable
nested virtualization -- needed if all one has is the free bits from VMWare.

# The Process

1. Enable SSH access to the ESXi server.
2. Create an ESXi VM for the initial, outer guest.
3. Shutdown the ESXi VM.
4. ***Edit the VM's .vmx file, adding "vhv.enable = TRUE".***
5. Done.

## 1. Enable SSH access to the ESXi Server

If you have not already done so, this process will require direct access to the
ESXi instance's configuration.  VMWare often calls this "Tech Support Mode".
This can be done from the ESXi host's console, or through the vSphere Client.
See the appendix in this document titled, `Enabling SSH access to ESXi 5.5`_,
for more detailed instructions on how to enable SSH access.


## 2. Create an ESXi VM

Create an ESXi VM for the initial, outer guest.  VMWare 'virtual machine
version' 8 or greater should be used; this is the default for ESXi 5.5.  Install
the operating system, (Linux), nothing special here, just perform a normal
install; ensure the installed OS is 64 bit.  Do make sure to provision the disk
with enough space for the nested OS's virtual disk.  An appropriate amount of
CPU and memory will also be needed.  The first time you attempt this I recommend
over provisioning all three: disk, memory, and CPU.  As I was experimenting I
found that the nested OS ran notably slower; giving everything extra resources
seemed to improve performance.  I am still experimenting with fine tuning
resource overheads.  Generally I'm finding that virtualized components do behave
as advertised, but default configurations on install do need some finer tuning
-- in short, no surprises.

## 3. Shutdown the ESXi VM

With an ESXi VM configured and installed with an operating system, you are ready
to (re)configure the VM to allow nested virtualization.  The reconfiguration
will happen to the VM's definition, and as a consequence, the VM needs to be in
the stopped state.  ESXi, as all others I'm aware of, does not let you
(virtually) modify the hardware while the VM is running.  Stop the ESXi VM that
will be reconfigured to support nested virtualization.

## ***4. Edit the VM's Configuration***

This step is the critical step.  The ESXi VM must be shutdown, as noted
previously; if it is not the change will be reverted by ESXi.  Fundamentally,
the change is simple:  add the configuration setting ``vhv.enable = "TRUE"`` to
the configuration.  This must be added to the VM's ``.vmx`` file.

SSH into the ESXi server and then locate and edit the VM's .vmx file:

```bash
> find / -name \*.vmx
> echo 'vhv.enable = "TRUE"' >> /path/to/host.vmx
```

## 5. Done

Once the change to the VM's configuration is effected, simply boot the VM and
use VirtualBox within the ESXi VM to create a nested VM.

Note:  You should be able to create 64 bit, and multiple processor/core VM's, up
to the limits of the ESXi VM's resources.  If the (re)configuration was not
successful then it is likely that VirtualBox will allow you to create a VM, but
that VM will be restricted to 32 bit and will not support multiple processors -
this is a specific pattern I noted prior to discovering the correct process for
ESXi 5.5.  Earlier versions of ESXi have a different process, not described
here, and without my crystal ball, I'm at a loss for future versions.

----

# Extra Credit

In discovering the above process, which I distilled to what I felt was the
minimum, for simplicity, I made a few "superfluous" discoveries.  So that the
above process may be more broadly applicable, an so that the reader is
more informed, I have detailed the "extras" here.

## Old Wives Tales

Technically not old wives tales, the following details are floating around in
blog postings and are no longer accurate, for ESXi 5.5.  At one point in time,
they were correct; I performed the process detailed here with out them as
verification that they were not necessary.

### `vhv.allow` vs. `vhv.enable`

Earlier versions of ESXi, possibly as late as early 5.x versions, used a
slightly different means of enabling nested virtualization.  The `vhv.allow`
parameter was applied to the ESXi server's configuration in
`/etc/vmware/config`.  This is not necessary, but does not conflict with the
per VM configuration detailed in this posting and required by ESXi 5.5.

### Editing the VM's CPU Preferences

In other postings on this subject I noted that an additional step involving
editing the VM's CPU Preferences was detailed.  Changing the "CPU/MMU Virtualization" from
'Automatic' to forced settings for Intel VT-x and hardware MMU virtualization
appears to no longer be required.  I have successfully nested VirtualBox 64 bit
VMs inside ESXi 5.5 VMs with the 'Automatic' setting.  Caveat:  I have found no official
documentation discussing this for 5.5 either way.


## ESXi Networking - Promiscuous Mode

Almost all of the writings I encountered that discuss nesting virtualization
with ESXi cite setting "networking" into promiscuous mode.  This is not a
requirement for nesting virtualization.  The basic example of nesting
VirtualBox, (using NAT), inside an ESXi Linux instance was executed with out
adjusting any ESXi network parameters.

Enabling promiscuous mode *is* required if your ESXi VM will nest virtual
machines that require bridge mode, sometimes evidenced by the fact that the
nested VM has a new ethernet MAC address.  Promiscuous mode, be it on ESXi, or
other technologies, is the means by which a network interface can receive
packets for hardware addresses, (MAC addresses), other than the one the
interface is assigned.

The most common nesting example I observed was ESXi inside ESXi.  In this case,
promiscuous mode would be necessary with the default ESXi networking
configuration because that model is a bridged model in which each VM is given a
newly allocated, and different, MAC address.


## Disk Performance

During my initial experimentation with nested VM's I observed a clear decrease
in performance of the nested VM.  My initial experimentation mostly only went as
far as installing the OS on the nested VM.  Installing an OS is generally a disk
intensive activity.

Disk virtualization is more expensive than most.  Nesting virtualized disks will
accumulate "virtualization debt" quicker than other virtualized components.  The
short, but rambling explanation goes something like this:

> In my inner VM I write a block to "disk".  This traverses the inner OS's
> file system code and is mapped to a sector on the inner VM's *virtual* block
> device.  Writing is the passed to the outer VM, traverses the file system
> code, and is mapped to the outer VM's *virtual* block device.  Finally, the
> block is passed to the host, (physical), file system, mapped through to a
> sector, and finally placed on the actual physical device.  -- If your head is
> spinning now, it should be.  That's **three** times the block is passed
> through file system code on it's eventual path to a physical write.

This problem is understood in the virtualization community, and there are
methods for avoiding differing degrees of the penalty based on the requirements
of an installation.  I will not cover these here.  My point:  if your nested
VM's strike you as slow, this may be a significant part of the why.

Armed with the above understanding, I set out to make things run a bit smoother,
i.e. faster.  Here are a few ideas I had; some I carried out successfully, some
are on my "to try" list:

1. Enabling "Host I/O Caching".  This seemed to help and was quick to try.
2. Giving each virtualized device some 'room to breath' eases the pressure.
   Some extra CPU and memory felt like it helped.
3. Using alternative "devices" for disk should help as well, I haven't tried
   this yet.
   - Raw disk device, by passing the virtualization of the device completely.
   - iSCSI


----

# Appendix

## Enabling SSH access to ESXi 5.5

ESXi supports direct SSH access to the server running ESXi.  This mechanism is
referred to in VMWare documentation as "Tech Support Mode".  VMWare has a
[Knowledge Base][kb] article elaborating the process for a range of versions:
[KB article 1017910][kb-1017910]

[kb]: http://kb.vmware.com/
[kb-1017910]: http://kb.vmware.com/kb/1017910

Here is the verbal description to enable SSH to the ESXi server from the Windows
vSphere (thick) Client:

1. Select the server's Configuration tab.  Select the server, not a child VM,
   from the left hand side and then select the 'Configuration' tab across the
   top.
2. Select the 'Security Profile' from the Software section on the left hand side
   of the Configuration tab.
3. Open the 'Services Properties' dialog window.  Click on the 'Properties...'
   link along the right hand side near the top in the 'Services' section of the
   Security Profile table.
4. Open the 'SSH Options' dialog.  In the 'Services Properties' dialog scroll
   down to the 'SSH' label and select it, (one click).  Then press the
   'Options...' button in the lower right corner of the dialog.
5. Use the 'SSH Options' dialog to enable SSH by choosing "Start and stop with
   host".  The SSH service can also be started immediately with the 'Start'
   button.
6. Access the host by ssh'ing to the IP or hostname of the ESXi server and
   logging in with an appropriate account.  The 'root' user and password created
   during ESXi initial installation will work.
