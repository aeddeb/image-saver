def test_base_route(app):
    url = '/'
    about_url = '/about'

    response = app.get(url)
    response_about = app.get(about_url)

    assert b'Welcome to the Image Saver App!' in response.get_data() 
    assert response.status_code == 200

    assert b'For details about the development of this app' in response_about.get_data()
    assert response_about.status_code == 200