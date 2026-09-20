import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/"PortMaster"),str(ROOT/"PortMaster"/"pylibs"),str(ROOT/"PortMaster"/"exlibs")]
from harbourmaster.harbour import register_source
class TestSourceOwnership(unittest.TestCase):
 def test_duplicate_prefix_cannot_take_over(self):
  sources={};first=object();register_source(sources,"xw",first,"first.json")
  with self.assertRaisesRegex(ValueError,"Duplicate source prefix"):register_source(sources,"xw",object(),"second.json")
  self.assertIs(sources["xw"],first)
 def test_distinct_prefixes_coexist(self):
  sources={};register_source(sources,"pm",1,"pm.json");register_source(sources,"xw",2,"xw.json")
  self.assertEqual(sources,{"pm":1,"xw":2})
if __name__=="__main__":unittest.main()
