import json,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/"PortMaster"),str(ROOT/"PortMaster"/"pylibs"),str(ROOT/"PortMaster"/"exlibs")]
from harbourmaster.xiaoweios_localization import load_overlay,localize_port_info,validate_overlay
def overlay():
 return {"schema":"xiaoweios.ports.localization.v1","locale":"zh_CN","upstream":{"url":"official","sha256":"a"*64},"entries":{"portmaster:demo.zip":{"source_title":"Demo","title":"演示","description":"中文描述","instructions":"","review":"machine-assisted","provenance":{"method":"agent-assisted","reference":"test"}}}}
def info():return {"name":"demo.zip","attr":{"title":"Demo","desc":"English","inst":"Supply data"},"source":{"url":"https://example.invalid/demo.zip","md5":"a"*32}}
class TestXiaoweiOSLocalization(unittest.TestCase):
 def test_localizes_only_presentation_and_keeps_source_metadata(self):
  original=info();result=localize_port_info("demo.zip",original,validate_overlay(overlay()))
  self.assertEqual(result["attr"]["title"],"演示");self.assertEqual(result["attr"]["desc"],"中文描述");self.assertEqual(result["attr"]["inst"],"Supply data")
  self.assertEqual(result["attr"]["title_aliases"],["Demo"]);self.assertEqual(result["source"],original["source"]);self.assertEqual(original,info())
 def test_source_title_drift_and_missing_entry_fall_back(self):
  changed=info();changed["attr"]["title"]="Demo Changed"
  self.assertEqual(localize_port_info("demo.zip",changed,overlay()),changed)
  self.assertEqual(localize_port_info("other.zip",info(),overlay()),info())
 def test_loader_requires_active_locale_and_fails_closed(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/"zh_CN.json";path.write_text(json.dumps(overlay()),encoding="utf-8")
   self.assertIsNone(load_overlay(path,"en_US"));self.assertEqual(load_overlay(path,"zh_CN"),overlay())
   path.write_text("not json");self.assertIsNone(load_overlay(path,"zh_CN"))
 def test_install_metadata_is_rejected(self):
  value=overlay();value["entries"]["portmaster:demo.zip"]["artifact"]={}
  with self.assertRaises(ValueError):validate_overlay(value)
if __name__=="__main__":unittest.main()
