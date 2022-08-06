import pytestimport globimport functions as fcimport data as dtimport numpy as np#from numpy import testingdef pytest_generate_tests(metafunc):    """Generating parameters for tests"""    if "fileName" in metafunc.fixturenames:        filelist = glob.glob('test-files/*.xyz')        metafunc.parametrize("fileName", filelist )    if "angle" in metafunc.fixturenames:        rd_angle = np.random.uniform(-360.,360., 3)        metafunc.parametrize('angle', [rd_angle])    if "modnt" in metafunc.fixturenames:        rd_modnt = np.random.uniform(-100000.,100000., 3)        metafunc.parametrize('modnt', [rd_modnt])    if "cell_vec" in metafunc.fixturenames:        rd_cell_vec = np.random.uniform(-10.,100., 3)        metafunc.parametrize('cell_vec', [rd_cell_vec])    if "cell_ang" in metafunc.fixturenames:        rd_cell_ang = np.random.uniform(0.,180., 3)        metafunc.parametrize('cell_ang', [rd_cell_ang])    if "modnre"  in metafunc.fixturenames:        rd_modnre = np.random.randint(1, 3, 3)        metafunc.parametrize('modnre', [rd_modnre])                @pytest.fixture  def retreive_data(fileName):    """Get data from .xyz files"""    data = np.genfromtxt(fileName, skip_header=2, dtype='str')    el = data[:,0]    a = data[:,1].astype(float)    b = data[:,2].astype(float)    c = data[:,3].astype(float)    return(el, a, b, c)#@pytest.mark.skip#@pytest.mark.parametrize('modnt', [np.array([2., 7., 20.]),                                    #np.array([-10., 70000., 0.])])def test_trasla(retreive_data, modnt):    '''Checking that trasla actually translates'''    el, a, b, c = retreive_data        a_test = a+modnt[0]    b_test = b+modnt[1]    c_test = c+modnt[2]    #print('DATAAAAA test' , a_test, b_test, c_test)        a_out, b_out, c_out = fc.trasla(a, b, c, modnt)        #print('DATAAAAA trasl', a_tr, b_tr, c_tr)    assert a_out.shape == a.shape    assert b_out.shape == b.shape    assert c_out.shape == c.shape        np.testing.assert_array_almost_equal(a_out, a_test)    np.testing.assert_array_almost_equal(b_out, b_test)    np.testing.assert_array_almost_equal(c_out, c_test)    #@pytest.mark.parametrize('angle', [np.array([2., 7., 20.]),                                   # np.array([-10., 70000., 0.])])def test_angle_rad(angle):    ''' Checking that the function angle_rad transforms the angles into radians'''        print('ANGLE RANDOM', angle)        angle_test=np.zeros(len(angle))    for i in range(len(angle)):        angle_test[i] = angle[i]*np.pi/180            angle_out = dt.angle_rad(angle)             assert angle_out.shape == (3,)    np.testing.assert_array_almost_equal(angle_out, angle_test)    #@pytest.mark.skipdef test_angle_deg(angle):    ".Checking whether angle_rad is inversible"        angle_test = angle        angle_out = dt.angle_rad(angle)    for i in range(len(angle)):        angle_out[i] *= 180/np.pi                np.testing.assert_array_almost_equal(angle_out, angle_test)#@pytest.mark.skipdef test_r_matrix(angle):    "checking test_r matrix returns 3 3x3 matrices"        R1, R2, R3 = fc.r_matrix(angle)            assert R1.shape == (3,3)    assert R2.shape == (3,3)    assert R3.shape == (3,3)    #@pytest.mark.skip    @pytest.mark.parametrize('var', [True, False])def test_ruota(retreive_data, var, angle):        el, a_iniz, b_iniz, c_iniz = retreive_data    angle_rad = dt.angle_rad(angle)                    # print('A_iniz', a_iniz)            #print('A_TEST-inix', a_test)        #taking the initial mean position    if var == True:        a0_test = np.mean(a_iniz)        b0_test = np.mean(b_iniz)        c0_test = np.mean(c_iniz)                R1, R2, R3 = fc.r_matrix(angle_rad)        #constructing Rxyz matrix    # Rxy = np.dot(R1, R2)    # Rxyz = np.dot(Rxy, R3)        a_test = np.zeros(len(el))    b_test = np.zeros(len(el))    c_test = np.zeros(len(el))        #rotating one atom at the time    for j in range(len(el)):                #coordinates for atom one         x = [a_iniz[j],b_iniz[j],c_iniz[j]]        Rxy = np.dot(R1, R2)        Rxyz = np.dot(Rxy, R3)        x_rot= np.dot(Rxyz, x)                #assigning rotated coordinates to the first atom        a_test[j] = x_rot[0]        b_test[j] = x_rot[1]        c_test[j] = x_rot[2]             #shifting the molecule if var=true    if var == True :            a1_test =np.mean(a_test)        b1_test =np.mean(b_test)        c1_test =np.mean(c_test)        # print("A1-A0-test", a1_test-a0_test)        # print("B1-B0-test", a1_test-a0_test)        # print("C1-C0-test", a1_test-a0_test)        a_test = a_test - (a1_test-a0_test)        b_test = b_test - (b1_test-b0_test)        c_test = c_test - (c1_test-c0_test)        # print('A_TEST-final', a_test)    # print('A-INIZ-final', a_iniz)            a_out, b_out, c_out = fc.ruota(a_iniz, b_iniz, c_iniz, angle_rad, var)        # print('A-OUT', a_out)        np.testing.assert_array_almost_equal(a_out, a_test)    np.testing.assert_array_almost_equal(b_out, b_test)    np.testing.assert_array_almost_equal(c_out, c_test)    #@pytest.mark.skip#@pytest.mark.parametrize('cell_vec', [np.array([1., 1., 1.]),                                     #np.array([90000., 56., 2345.])])#@pytest.mark.parametrize('cell_ang', [np.array([87., 90., 90.]),                                    #np.array([9000000., -78., -90.])])#@pytest.mark.xfail(raises=ValueError)def test_cell(cell_vec, cell_ang):    "Check whether we get matrix elements to build the unit cell"        try:                angle_rad = dt.angle_rad(cell_ang)        print(angle_rad)            cell_vec_x_out, cell_vec_y_out, cell_vec_z_out = fc.cell(cell_vec, angle_rad)                assert cell_vec_x_out.shape == (3,)        assert cell_vec_y_out.shape == (3,)        assert cell_vec_z_out.shape == (3,)            if angle_rad[2] == np.pi/2:                    cell_vec_x_test = np.array([cell_vec[0], 0., 0.])            cell_vec_y_test = np.array([0., cell_vec[1], 0.])                    np.testing.assert_array_almost_equal(cell_vec_x_out, cell_vec_x_test)            np.testing.assert_array_almost_equal(cell_vec_y_out, cell_vec_y_test)                elif angle_rad[2] == np.pi/2 and angle_rad[0] == np.pi/2 and angle_rad[1] != np.pi/2:                    cell_vec_z_test = np.array([cell_vec[2]*np.cos(angle_rad[1]), 0., cell_vec[2]*(1-(np.cos(angle_rad[1]))**(0.5))])                    np.testing.assert_array_almost_equal(cell_vec_z_out, cell_vec_z_test)                elif angle_rad[2] == np.pi/2 and angle_rad[1] == np.pi/2 and angle_rad[0] != np.pi/2:                    cell_vec_z_test = np.array([cell_vec[2]*np.cos(angle_rad[0]), 0., cell_vec[2]*(1-(np.cos(angle_rad[0]))**(0.5))])            np.testing.assert_array_almost_equal(cell_vec_z_out, cell_vec_z_test)            elif angle_rad[2] == np.pi/2 and angle_rad[1] == np.pi/2 and angle_rad[0] == np.pi/2:                    cell_vec_z_test = np.array([0., 0., cell_vec[2]])                    np.testing.assert_array_almost_equal(cell_vec_z_out, cell_vec_z_test)            else:                    cell_vec_x_test = np.array([cell_vec[0], 0., 0.])            cell_vec_y_test = np.array([cell_vec[1]*np.cos(angle_rad[2]),cell_vec[1]*np.sin(angle_rad[2]) , 0.])                            np.testing.assert_array_almost_equal(cell_vec_x_out, cell_vec_x_test)            np.testing.assert_array_almost_equal(cell_vec_y_out, cell_vec_y_test)                            except ValueError:        pytest.xfail('ValueError')        pass #@pytest.mark.skip       #@pytest.mark.parametrize('cell_vec', [np.array([1., 1., 1.])])                                    #np.array([900., 56., 23.])])#@pytest.mark.parametrize('cell_ang', [np.array([90., 90., 90.]),                                  # np.array([9000000., -78., -90.])])#@pytest.mark.parametrize('modnre', [np.array([1, 1, 1])])#,                                    #np.array([2, 4, 5])])        def test_replica(cell_vec, cell_ang, modnre, retreive_data):        try:        el_iniz, a_iniz, b_iniz, c_iniz = retreive_data            angle_rad = dt.angle_rad(cell_ang)            cell_vecs_x, cell_vecs_y, cell_vecs_z = fc.cell(cell_vec, angle_rad )            N = len(el_iniz)                 M = N*modnre[0]*modnre[1]*modnre[2]                        a_test = np.zeros(len(el_iniz))        b_test = np.zeros(len(el_iniz))        c_test = np.zeros(len(el_iniz))        el_test = np.zeros(len(el_iniz))            for nat in range(len(el_iniz)):            for i in range(modnre[0]):                for j in range(modnre[1]):                    for k in range(modnre[2]):                                dx = i*cell_vecs_x[0] + j*cell_vecs_y[0] + k*cell_vecs_z[0]                        dy = i*cell_vecs_x[1] + j*cell_vecs_y[1] + k*cell_vecs_z[1]                        dz = i*cell_vecs_x[2] + j*cell_vecs_y[2] + k*cell_vecs_z[2]                                a_test = np.append(a_test, a_iniz[nat]+dx)                        b_test = np.append(b_test, b_iniz[nat]+dy)                        c_test = np.append(c_test, c_iniz[nat]+dz)                        el_test = np.append(el_test, el_iniz[nat])                        el_out, a_out, b_out, c_out = fc.replica (el_iniz, a_iniz, b_iniz, c_iniz, modnre, cell_vec, angle_rad)                assert M == len(el_out)                np.testing.assert_array_almost_equal(a_out, a_test[N:])        np.testing.assert_array_almost_equal(b_out, b_test[N:])        np.testing.assert_array_almost_equal(c_out, c_test[N:])           except ValueError:        pytest.xfail('ValueError')        pass    # except Exception:    #     pytest.xfail('Exception')    #     pass