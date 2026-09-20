import sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/"PortMaster"),str(ROOT/"PortMaster"/"pylibs"),str(ROOT/"PortMaster"/"exlibs")]
import harbourmaster
class TestXiaoweiOSPlatform(unittest.TestCase):
 def test_platform_is_explicit_and_os_managed(self):
  cls=harbourmaster.HM_PLATFORMS["xiaoweios"]
  self.assertEqual(cls.__name__,"PlatformXiaoweiOS");self.assertFalse(cls.MANAGER_UPDATES);self.assertEqual(cls.ES_NAME,"ports")
 def test_existing_and_unknown_platform_selection_remain(self):
  self.assertIn("rocknix",harbourmaster.HM_PLATFORMS);self.assertIn("default",harbourmaster.HM_PLATFORMS)
 def test_environment_and_downstream_identity_gate_manager_updates(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)
   self.assertFalse(harbourmaster.manager_updates_allowed({"XIAOWEIOS_PORTMASTER_OS_MANAGED":"1"},root))
   self.assertTrue(harbourmaster.manager_updates_allowed({},root))
   (root/"xiaoweios-downstream.json").write_text("{}")
   self.assertFalse(harbourmaster.manager_updates_allowed({},root))
if __name__=="__main__":unittest.main()
