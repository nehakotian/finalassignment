dict_update = {"old_id": 2,
               "class_id": 1,
               "class_leader": "Yes",
               "student_id": 2,
               "student_name": "sarvesh",
               "selected_id": 2,
               "name": "neha"}

dict_new = {
    "class_leader": "No",
    "name": "Ratan",
    "selected_id": 3}

dict_new_class = {
    "class_name": "BE EXTC A"
}

dict_delete = {"id": 15}


def test_home(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/?name="Neha"')
    assert resp.status_code == 200


def test_show_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/show_class')
    assert resp.status_code == 200


def test_new(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new', data=dict_new)
    assert resp.status_code == 302


def test_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update_student', data=dict_update)
    assert resp.status_code == 200


def test_show_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update', data=dict_update)
    assert resp.status_code == 302


def test_new_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_class', data=dict_new_class)
    assert resp.status_code == 302


def test_delete(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/delete', data=dict_delete)
    assert resp.status_code == 302
