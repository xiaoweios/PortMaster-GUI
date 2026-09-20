import sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/"PortMaster"),str(ROOT/"PortMaster"/"pylibs"),str(ROOT/"PortMaster"/"exlibs")]
from harbourmaster import source_defaults
from harbourmaster.harbour import register_source, sync_xiaoweios_source
class TestSourceOwnership(unittest.TestCase):
 def test_duplicate_prefix_cannot_take_over(self):
  sources={};first=object();register_source(sources,"xw",first,"first.json")
  with self.assertRaisesRegex(ValueError,"Duplicate source prefix"):register_source(sources,"xw",object(),"second.json")
  self.assertIs(sources["xw"],first)
 def test_distinct_prefixes_coexist(self):
  sources={};register_source(sources,"pm",1,"pm.json");register_source(sources,"xw",2,"xw.json")
  self.assertEqual(sources,{"pm":1,"xw":2})
 def test_xiaoweios_source_is_explicit_and_https_only(self):
  self.assertNotIn("030_xiaoweios.source.json",source_defaults({}))
  configured=source_defaults({"XIAOWEIOS_PORTS_SOURCE_URL":"https://ports.xiaoweios.org/ports.json"})
  self.assertIn("030_xiaoweios.source.json",configured);self.assertIn('"prefix": "xw"',configured["030_xiaoweios.source.json"])
  with self.assertRaises(ValueError):source_defaults({"XIAOWEIOS_PORTS_SOURCE_URL":"http://bad/ports.json"})
 def test_os_owned_source_is_updated_or_removed_without_touching_user_source(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);user=root/"900_user.source.json";user.write_text("user")
   defaults=source_defaults({"XIAOWEIOS_PORTS_SOURCE_URL":"https://ports.xiaoweios.org/ports.json"})
   sync_xiaoweios_source(root,defaults);managed=root/"030_xiaoweios.source.json";self.assertTrue(managed.is_file())
   sync_xiaoweios_source(root,source_defaults({}));self.assertFalse(managed.exists());self.assertEqual(user.read_text(),"user")
if __name__=="__main__":unittest.main()
