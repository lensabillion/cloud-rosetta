# Databases: Read Scaling and Surviving Failure

**Goal:** choose a database deployment based on what must keep working.
Prerequisite: [the first application](00-landscape.md). A database stores structured information
that the application needs to query or change, such as the owner and caption of a photo.

## Three Different Questions

- **Availability:** can the application recover when a machine or zone fails?
- **Read scaling:** can reporting queries run somewhere other than the writer?
- **Recovery:** can we restore data after a mistake, deletion, or larger outage?

A replica is a copy. That word alone tells you neither whether clients can read it nor whether
it can become the writer automatically. Replication also copies many mistakes; it is not a
substitute for backups and a tested restore procedure.

## Read the Deployment Type

| Deployment | Read from the secondary? | What to check |
| --- | --- | --- |
| RDS Multi-AZ DB instance | No | Standby exists for failover |
| RDS Multi-AZ DB cluster | Yes, two readable standbys | Supported engines and versions; standby can take over |
| Ordinary RDS read replica | Yes | Asynchronous lag and promotion process; not automatic HA by itself |
| Azure SQL Database | Tier-dependent | Zone redundancy, read scale-out, and Hyperscale configuration |
| Azure SQL active geo-replication | Yes | Asynchronous copy; failover orchestration is a separate decision |
| Cloud SQL for MySQL regional HA | HA standby is not a read endpoint | Automatic failover; add read replicas separately when needed |

Sources: [RDS deployment types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html),
[RDS read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html),
[Azure local and zone redundancy](https://learn.microsoft.com/en-us/azure/azure-sql/database/high-availability-sla),
[Azure geo-replication](https://learn.microsoft.com/en-us/azure/azure-sql/database/active-geo-replication-overview),
[Cloud SQL MySQL HA](https://docs.cloud.google.com/sql/docs/mysql/high-availability).

## Before and After a Zone Failure

![A two-zone standby design before and after failover; a separate read-replica branch does not by itself provide automatic failover.](assets/database-failover.svg)

The drawing illustrates a primary/standby pattern, not every database deployment. The application
must reconnect and retry safely during failover. A region-wide outage needs a separate recovery
plan. Do not label a single-region standby diagram “disaster recovery” without defining the disaster.

## Work Through a Decision

Your photo application's database uses an RDS Multi-AZ **DB instance**. A slow reporting query
must move away from the primary. Can it run on the existing standby?

<details><summary>Reveal the answer</summary>

No. That standby does not serve reads. Evaluate a read replica, a different deployment such as a
supported Multi-AZ DB cluster, or a separate analytics path. Keep the availability requirement
while deciding how much replication lag reporting can tolerate. “Multi-AZ is never readable”
is also wrong: the DB cluster deployment has readable standbys.

</details>

**Change one constraint:** the database must keep writes available after a zone failure. Adding
an ordinary asynchronous read replica alone is not enough to claim automatic failover. Specify
how failover happens, how clients reconnect, and what data-loss window is acceptable.

**Next:** [database comparisons](05-databases.md) · [practice scenarios](practice.md) ·
[storage](README.md).

<!-- This document follows common-doc-guidelines.md. -->
