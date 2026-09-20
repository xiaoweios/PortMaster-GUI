import sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/"PortMaster"),str(ROOT/"PortMaster"/"pylibs"),str(ROOT/"PortMaster"/"exlibs")]
from harbourmaster.harbour import HarbourMaster
class Callback:
 def __init__(self):self.messages=[]
 def message_box(self,text,*a,**k):self.messages.append(str(text))
class Platform:MANAGER_UPDATES=False
class TestManagerUpdates(unittest.TestCase):
 def test_manager_archive_is_rejected_and_temporary_download_removed(self):
  hm=object.__new__(HarbourMaster);hm.platform=Platform();hm.callback=Callback()
  with tempfile.TemporaryDirectory() as td:
   archive=Path(td)/"PortMaster.zip";archive.write_bytes(b"not installed")
   self.assertEqual(hm._install_portmaster(archive,do_delete=True),255)
   self.assertFalse(archive.exists());self.assertTrue(hm.callback.messages)
if __name__=="__main__":unittest.main()
