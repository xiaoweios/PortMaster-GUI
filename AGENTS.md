# XiaoweiOS PortMaster Downstream

This repository is a thin downstream of `PortsMaster/PortMaster-GUI`. Preserve
upstream formats and keep general fixes separable for upstreaming.

XiaoweiOS product behavior and support claims are owned by
`projects/xiaoweios/docs/specs/components/emulator_runtime/ports_support_spec.md`
in the parent `goindie2` repository. Do not define supported titles or device
claims here. On XiaoweiOS the manager is updated only through the OS package;
upstream manager self-update/restore/channel controls must remain unavailable.
Port and runtime catalog behavior remains upstream-owned unless a focused,
tested downstream change is required.

Run XiaoweiOS downstream tests with:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_xiaoweios_*.py' -v
```
