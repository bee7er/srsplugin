

Command line rendering:

        NB Since R21 you have to login to the command line every now and again:
        Commandline.exe g_licenseUsername=<your_user_name> g_licensePassword=<your_password>

        /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/srs_functions.c4d -frame 0 5 -oimage ~/Code/c4d/srs/frames/srs -omultipass ~/Code/c4d/test_mp -oformat TIFF
        /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/RedshiftTest.c4d -frame 0 5 -oimage ~/Code/c4d/srs/frames/srs -omultipass ~/Code/c4d/test_mp -oformat PNG
        /Applications/MAXON/Cinema\ 4D\ R20/Commandline.app/Contents/MacOS/Commandline -render ~/Code/c4d/srs/RedshiftTest.c4d -oimage ~/Code/c4d/srs/redshifttest/frames/redshifttest -omultipass ~/Code/c4d/test_mp


NB Running these tests from srsplugin folder:

        Testing with curl on the command line:
		        curl -X POST -H "Content-Type: application/json" -d '{"sequence": "poipoi", "from": 8, "to": 88}' http://srsapi.test/api1/renders/request

        Testing upload to master:

                # Uploading rendered frames to master
                # NB we must use the vagrant directory sequence
                    curl -v -F 'upload=@/home/vagrant/Code/srstest/srs/redshifttest/tars/RedshiftTestBePngs.tar.gz' \
                        -H "Content-Type: multipart/form-data" http://srsapi.test/results

        Testing download from master:

                curl --output ./projects/RedshiftTestBePngs.tar.gz http://srsapi.test/uploads/projects/RedshiftTestBe.c4d
