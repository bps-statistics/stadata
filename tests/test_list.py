import stadata as stat

def test_list_statictable(token):
    client = stat.Client(token)
    result_all = client.list_statictable()
    result_nasional = client.list_statictable(domain=['0000'])
    assert len(result_all)>len(result_nasional)
    
def test_list_dynamictable(token):
    client = stat.Client(token)
    result_all = client.list_dynamictable()
    result_nasional = client.list_dynamictable(domain=['0000'])
    assert len(result_all)>len(result_nasional)
    
def test_list_pressrelease(token):
    client = stat.Client(token)
    result_all = client.list_pressrelease()
    result_nasional = client.list_pressrelease(domain=['0000'])
    assert len(result_all)>len(result_nasional)
    
def test_list_publication(token):
    client = stat.Client(token)
    result_all = client.list_publication()
    result_nasional = client.list_publication(domain=['0000'])
    assert len(result_all)>len(result_nasional)