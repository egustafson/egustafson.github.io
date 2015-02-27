:title: IPv6 Tunneling over IPv4 Networks
:date: 2015-02-25
:slug: ipv6-tunneling
:author: Eric Gustafson
:tags: IPv6, Tunneling, NAT, RFC2893, FreeBSD, Linux
:status: draft

------------------------------------
Connecting to the v6 world from afar
------------------------------------

It turns out that proposing IPv6 as a "solution" for various networking problems
in the Cloud and Container, read 'Docker', spaces opens a small Pandora's Box of
questions.  This article is the first in a series discussing pragmatic IPv6
issues along side multiple environments using it.  The goal of exploring IPv6 in
these articles is to solve, or provide possible solutions, to problems.

Motivations
===========

A while ago I took it upon myself to add my home "lab" environment to the public
IPv6 network.  IPv6_ **is** coming, and it behooves any technologist to gain
practical experience.  While IPv6 is just the next version after IPv4_,
there are sharp edges and I certainly found a few.  Unfortunately, I let the v6
portion of my network acquire some bit-rot over time and then found myself
needing to resurrect the project.  Additionally, there were some problems I had
encountered and never fully tackled -- time to reset and start fresh.  There are
certainly a couple of learning curves to operating an IPv6 network, it is a bit
more than **just** the next version of IP_.

.. _IPv6: https://en.wikipedia.org/wiki/IPv6
.. _IPV4: https://en.wikipedia.org/wiki/IPv4
.. _IP: https://en.wikipedia.org/wiki/Internet_Protocol

Lately I have been repeatedly working with different virtualized compute
environments: OpenStack Nova, Amazon Web Services, and Docker are all in the
list.  A recurring theme in interconnecting nodes is to apply a liberal use of
NAT_.  NAT is not a solution, NAT is, in my opinion, a plague.  NAT was created
as a response to the depleting IPv4 address space and it seems to have devolved
into a hammer and we now have a generation of software developers that only see
nails. 

.. _NAT: https://en.wikipedia.org/wiki/Network_address_translation

The solution, in the truly abstract sense, is IPv6, and NAT was the hack.  So,
one day recently it dawns on me when looking at yet another Docker networking
project, "flatten the network, it should be flat, and adopt the protocol that
was, and is the solution:  IPv6".

Following this reasoning, with the help of the team I work with, we set out to
build a reusable environment with not only IPv6 support, but specifically the
ability to run an IPv6 only environment.  Very quickly after defining this goal,
it became obvious that connectivity between test environments, and for that
matter, into the public IPv6 Internet would be highly desirable.  And there we
are:  "how do we connect private, and possibly isolated behind NAT, networks to
the public IPv6 Internet?"

There are many, many, articles written about the mechanics of connecting to the
IPv6 Internet.  What I was unsuccessful in finding is a description of how such
connections worked, if it was possible to transition NAT, and what the possible
issues in NAT traversal might be.  The information is out there, but not in a
distilled form; I will attempt to provide such a distillation here.


IPv6 Primers
============

*(Note: this section really belongs in a separate article as a preface to my IPv6
series; don't be surprised if it moves.)*

All software, and almost all networking people I talk to are aware of IPv6 and
have a mental model of what IPv6 is.  It generally goes something along the
lines of, "it's IPv4 with longer addresses".  The slightly more astute will also
add that this requires a new record type in DNS, the AAAA record.  This is all
true, however "the devil is in the details", and v6 is no exception.  The
following sections elaborate a few of the subtle, but important "details" worth
noting when beginning work with IPv6.  

Prefix Length - Subnetting
--------------------------

The concept of subnetting, or splitting an address into two sections, the
'network' and 'host' address, remains the same; the implementation differs.  In
IPv4 addresses blocks were initially classified as Class 'A', 'B', and 'C'[*]_
and later we moved to CIDR ("`Classless Inter-Domain Routing`_") where the
boundary between network and host was any bit boundary in the 32 bit space of the
IPv4 address.  Often a "larger" block, CIDR boundary to the left, more
significant bits, would be handed to an organization and they would define a new
CIDR bit location within the host space and subdivide the network, aka
"subnetting".

IPv6 uses the same concept, however the boundary between network and host
sections of the address is fixed.  An IPv6 address is 128 bits and the lower 64
are the host segment.  This leaves 64 bits of network address.  Unlike
configuring IPv4 network interfaces where the "netmask" must be specified, an
IPv6 configuration does not need to specify the netmask, it is always 64 bits.

Subdividing IPv6 address space does still happen, it happens above the first 64
bits in the address.  For instance the IPv4 address to IPv6 network mapping
specifies that each IPv4 address is associated with an IPv6 network that can be
further subdivided.  The v4 to v6 mapping provides a "/48" network for each v4
address meaning that each 6to4 network has 65536 subnets or 16 remaining bits to
subnet in the 64 bit network portion of and IPv6 address, (48 + 16 = 64).

A quick note on terminology.  In IPv4 the term 'subnet mask', or 'netmask' is
used when describing the bit boundary between network and host address segments.
In IPv6 a new term has evolved, "prefix length", sometimes abbreviated,
"prefixlen".  The prefix length is meant to describe the number of bits that are
fixed in an allocated block of IPv6 addresses.  This is similar, but subtly
different than a netmask.  The netmask in IPv6 is always /64.  If I am given a
network block with prefix length /48 (48 bits) then I have 16 bits, or 65536
discrete networks I can allocate from.  If I am given a prefix length of /64
then I have exactly *one* IPv6 network and can not subdivide it.

.. _Classless Inter-Domain Routing:
   https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing 

.. [*] There were additional Classes, 'D' and 'E'.
       https://en.wikipedia.org/wiki/Classful_network#Introduction_of_address_classes


Tunneling - RFC-4213
====================

`RFC 4213`_ specifies, "IPv4 compatibility mechanisms that can be implemented
by IPv6 hosts and routers."  The document specifically details a method for
transporting IPv6 packets across an IPv4 only network -- tunneling.  The RFC
does not exclude other methods, however the method in RFC 4213 is trivially
simple and in wide use on the public (IPv4) Internet.  

.. _RFC 4213: https://www.ietf.org/rfc/rfc4213.txt

To me, at least, the obvious way to tunnel v6 packets through a v4 network is to
simply wrap the v6 packet in a v4 packet and send it to the other end of the
tunnel.  This is exactly what RFC 4213 details::

                             +-------------+
                             |    IPv4     |
                             |   Header    |
    +-------------+          +-------------+
    |    IPv6     |          |    IPv6     |
    |   Header    |          |   Header    |
    +-------------+          +-------------+
    |  Transport  |          |  Transport  |
    |   Layer     |   ===>   |   Layer     |
    |   Header    |          |   Header    |
    +-------------+          +-------------+
    |             |          |             |
    ~    Data     ~          ~    Data     ~
    |             |          |             |
    +-------------+          +-------------+

           Encapsulating IPv6 in IPv4

The IPv6 packet is unmodified and an IPv4 header is prepended -- simple.  The
source and destination v4 addresses are the tunnel endpoints.  The IP protocol
number is 41.  All remaining fields in the IPv4 header are calculated using the
IPv6 packet as the v4 payload.

There is virtually no 'protocol' between the two tunnel endpoints; no handshake
is required with this method.  Each endpoint is configured to know the IPv4
address of the other and encapsulates any IPv6 packet it is handed.  The tunnel
endpoint is treated as a virtual interface and can be used in routing
configurations like any other interface.

IPv4 NAT Ramifications
----------------------

Can an RFC 4213 tunnel be established with one endpoint behind IPv4 NAT?  Based
on RFC 4213's specification there are no barriers.  In practice:  yes, RFC 4213
tunnel endpoints can live behind a NAT'ing device.

How does RFC 4213 tunneling work when one endpoint is behind a tunnel?  First,
the remote endpoint must be configured with the exposed, or post-NAT'ed, or
public IPv4 address; this allows inbound packets to be properly delivered to the
NAT device.  Second, the local, NAT'ed endpoint should be configured with the
proper remote IPv4 address and the hidden, private, IPv4 address of the tunnel
device.  As the packet transitions the NAT device the private IPv4 address will
be rewritten to the public address and forwarded.  When the packet arrives at
the remote endpoint it will present as if it had come from the NAT device.

The NAT device must be configured such that it either remembers state, or has
bi-directional NAT.  If the NAT device is keeping state then a packet from
behind the NAT device must be sent before the NAT device will know where to
deliver remote packets to behind the NAT device.  Also, if keeping state, it is
possible for the NAT device to forget the private endpoint if the tunnel is idle
for longer than the timeout on state.  Bi-directional NAT configurations will
not suffer from these problems.  If no state is kept and bi-directional NAT is
not utilized then remote packets will be dropped at the NAT device and the
tunnel will not function properly.

Additionally, the NAT device must support NAT translation of IPv4 protocol 41
packets.  It has been reported that some consumer grade "home firewalls" are
configured by default to drop such packets.  Numerous other articles advise
checking such devices to ensure they are configured to pass this traffic.  I
have not discovered any citations of devices that would not, and could not pass
IPv4 protocol 41 traffic -- they could exist.

Small Details - What problems can occur
---------------------------------------

The ideal model of simply wrapping a v6 packet with a v4 header and sending it
on its merry way is great, but the astute reader will begin to identify a few
problems with this simplistic strategy.  In fact, there are a few details worth
mentioning.  In general, however, if the transit network and tunnel endpoints
are reasonably well behaved then the RFC 4213 tunnel performs well.

The following sections provide a light covering of each topic.  Complete details
can be found in `RFC 4213`_.

MTU
~~~

In the perfectly behaved case, IPv6 will use path MTU discovery and properly
determine the MTU.  The RFC 4213 endpoint will advertise an MTU that is the MTU
of the IPv4 transit network minus the size of the IPv4 header.  Everything will
just work.

RFC 4213 recommends a more conservative approach however.  The RFC recommends,
but does not require, advertising a static MTU of 1280.  This is the minimum
allowable size of an IPv6 packet.

ICMP and Tunnel Errors
~~~~~~~~~~~~~~~~~~~~~~

There are two categories of errors for which ICMP messages can exist.  ICMPv6
errors can originate on the far side of the tunnel, and ICMPv4 errors can occur
inside of the tunnel.

ICMPv6 errors are trivial to handle.  The ICMPv6 packet should transition the
tunnel, in reverse, just like any other IPv6 traffic.  End to end ICMPv6
functions normally and simply sees the tunnel as a single data link in the IPv6
network.

ICMPv4 errors in the tunnel pose a more complicated issue.  RFC 4213 states, in
short, that where meaningful ICMPv6 responses can be composed, they should, and
be forwarded to the IPv6 sender.  If ICMPv4 errors occur where there is no
meaningful way to alert the IPv6 sender then the packet and ICMPv4 response
should simply be dropped; both IPv4 and IPv6 are connectionless with no
guarantee of delivery.


Hop Limit
~~~~~~~~~

As stated in RFC 4213, "IPv6-over-IPv4 tunnels are modeled as a 'single-hop'
from the IPv6 perspective."  The encapsulated IPv6 packet does not have its hop
limit decremented while transiting the IPv4 network and only the IPv4 TTL is
manipulated in transit.  The IPv6 packet's hop limit is decremented by the
tunnel endpoint as if the IPv4 transit network is a single hop.


RFC-4213 Methods
================

The common name for *basic* RFC-4213 tunneling is \"6in4_\".  Utilizing the
techniques described above, manually configuring tunnel endpoints would be
described as 6in4.

.. _6in4: https://en.wikipedia.org/wiki/6in4

6to4
----

The \"6to4_\" method builds on 6in4 by providing automated configuration.
Tunneling is acomplished according to RFC-4213 and configuration details are
prescribed in RFC-3056_ and RFC-3068_.  In short, RFC-3056 reserves 2002::/16
for statically mapping IPv4 addresses to IPv6 networks and RFC-3068 specifies an
IPv4 Anycast address to be used as a tunnel endpoint.

.. _RFC-3056: https://www.ietf.org/rfc/rfc3056.txt
.. _RFC-3068: https://www.ietf.org/rfc/rfc3068.txt

The 2002::/16 IPv6 prefix is used to map public IPv4 addresses into an IPv6
network address.  The mapping is acomplished by concatinating 2002: with the 32
bit IPv4 address to form a /48 prefix length network for each IPv4 address.  The
result is depicted as such::

  2002:[IPv4 Addr]::/48

This pattern leaves 16 bits in the network portion of each IPv6 network for
subnetting.  

The addition of an IPv4 Anycast address, defined in RFC-3068, to be used for
tunneling completes the automation of configuration in the 6to4 scheme.  The
address is 192.88.99.1.  Routers sending 6to4 traffic into the public Internet
send to 192.88.99.1 and in reverse, routers send 2002::/48 traffic to the
embedded IPv4 address.  No explicit configuration of the 6to4 tunnel is needed.

There has been some criticism of 6to4 tunneling.  Two items I will call out are:

- No support for tunnel endpoints behind NAT.
- Non deterministic network routing, (and latency), because of Anycast usage.

Additional criticisms have been levied against the 6to4 scheme, including
additional RFC's (RFC-6343, RFC-3964).

In general, and with the availability of **free** 6in4 tunnel brokers, discussed
later, it is my recomendation to avoid the use of 6to4 with out specific reasons
for choosing it.

Teredo - RFC-4380
-----------------

For completeness, it is worth mentioning that Teredo_ is an additional method of
connecting to the public IPv6 network through a tunnel.  Teredo is **NOT** an
RFC-4213 based method.  Teredo uses UDP for encapsulation and does not tunnel
networks, but only single IPv6 hosts.  Teredo *does* allow transitioning NAT.
Using Teredo was popularized by its inclusion in Microsoft Windows; many Windows
users are connected to IPv6 networks and are not even aware of it.  There is
also a Linux/xxxBSD, open source client named Miredo_.

.. _Teredo: https://en.wikipedia.org/wiki/Teredo_tunneling
.. _Miredo: http://www.remlab.net/miredo/

Tunnel Brokers
==============

"Tunnel Broker" is the term being used to describe ISP's who will provide tunnel
access to the IPv6 public Internet.  There are a number of brokers, and among
them, a number that offer free access for tunneling IPv6.  The Wikipedia page,
"\"`List of IPv6 tunnel brokers`_\" contains a list.

.. _List of IPv6 tunnel brokers: https://en.wikipedia.org/wiki/List_of_IPv6_tunnel_brokers

The two most popular, and well deployed brokers are `Huricane Electric`_\ 's
(HE) \"`IPv6 Tunnel Broker`_\" service and SixXS_ (Six Access).  I chose HE
because they appeared to have more written about them and how to connect to
their tunnel broker.  In hindsight I have concluded that SixXS and HE are on
comparable footing.  I would recommend starting with one of the two, but believe
both are very comparable.

.. _Huricane Electric: https://www.he.net/
.. _IPv6 Tunnel Broker: https://tunnelbroker.net/
.. _SixXS: https://www.sixxs.net/

**Implementing an HE Tunnel with FreeBSD**
==========================================



Placing the tunnel behind NAT(v4)
---------------------------------

Firewall Rules
--------------

PFSense
-------

Linux?
------

But what about Linux?  All of the above can be accomplished using Linux. HE's
TunnelBroker site provides specifics for Linux, along with a number of
additional operating systems.  This article will not cover Linux -- sorry.

Conclusion
==========

6in4 Tunneling based on RFC-4213 is both a simple, and an effective method for
connecting IPv6 networks across IPv4, including NAT.  There are multiple IPv6
tunnel brokers offering free, and hastle free, tunnels using 6in4.  Modern, open
source operating systems have good support for 6in4.  There are open source
"firewall" appliances using these operating systems and providing simple 6in4
configuration.  Join the IPv6 network today, there's no reason to wait.  Better
yet, start using IPv6 to solve network problems induced by using IPv4.


References
==========

:IPv6 Tunneling:
   - https://en.wikipedia.org/wiki/IPv6
   - https://en.wikipedia.org/wiki/IPv6_transition_mechanisms
   - http://ipv6.com/articles/gateways/IPv6-Tunnelling.htm
     
:6in4:
   - https://en.wikipedia.org/wiki/6in4
   - http://www.sixscape.com/joomla/sixscape/index.php/ipv6-training-certification/ipv6-forum-official-certification/ipv6-forum-network-engineer-silver/network-engineer-silver-transition-mechanisms/tunnels/6in4-tunnel
:6to4:
   - https://en.wikipedia.org/wiki/6to4
   - http://www.sixscape.com/joomla/sixscape/index.php/ipv6-training-certification/ipv6-forum-official-certification/ipv6-forum-network-engineer-silver/network-engineer-silver-transition-mechanisms/tunnels/6to4-tunnel
:RFC 2893 - Transition Mechanisms for IPv6 Hosts and Routers:
   - obsoleted by RFC 4213
   - https://www.ietf.org/rfc/rfc2893.txt
:RFC 3056 - Connection of IPv6 Domins via IPv4 Clouds:
   - https://www.ietf.org/rfc/rfc3056.txt
:RFC 3068 - An Anycast Prefix for 6to4 Relay Routers:
   - https://www.ietf.org/rfc/rfc3068.txt
:RFC 4213 - Basic Transition Mechanisms for IPv6 Hosts and Routers:
   - https://www.ietf.org/rfc/rfc4213.txt
:RFC 4380 - Teredo\: Tunneling IPv6 over UDP through Network Address Translations (NATs):
   - http://www.ietf.org/rfc/rfc4380.txt
   - https://en.wikipedia.org/wiki/Teredo_tunneling
:Tunnel Broker (IPv6):
   - https://tunnelbroker.net/
:IPv6 Check:
   - http://www.test-ipv6.com/
   - http://ipv6-address.eu/
     

.. Local Variables:
.. fill-column: 80
.. End:
