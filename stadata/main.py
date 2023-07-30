import requests
import warnings
import pandas as pd
from tqdm import tqdm
import html
from .material import Material

BASE_URL = "https://webapi.bps.go.id/v1/"

class Client(object):
    """
    Object to connect with webapi
    """
    TOKEN = ""
    def __init__(self, token):
        """
        Initialize client object
        :param token: token from webapi website
        """
        self.TOKEN = token
    
    def __get_list(self,lang = 'ind',domain='0000',model='statictable',keyword='',page=1,var='',turvar='',vervar='',th='',turth='',month='',year=''):
        """
        Method to get list data based on model
        :param lang: Language to display data. Default value: ind. Allowed values: "ind", "eng"
        :param domain: Domains that will be displayed variable (see master domain on http://sig.bps.go.id/bridging-kode/index)
        :param model: Type data to display
        :param keyword: Keyword to search
        :param page: Page to display statictable
        :param var: Variable ID selected to display data
        :param turvar: Derived Variable ID selected to display data
        :param vervar: Vertical Variable ID selected to display data
        :param th: Period data ID selected to display data
        :param turth: Derived Period Data ID selected to display data
        :param month: Month of publication or press release in int
        :param year: Year of publication or press release
        """
        if(model=='data'):
            if(th != ''):
                url_th = '/th/'f'{th}'
            else:
                url_th = ''
            res = requests.get(f'{BASE_URL}api/list/model/'f'{model}/perpage/100000/lang/'f'{lang}/domain/'f'{domain}/key/'f'{self.TOKEN}/keyword/'f'{keyword}/page/'f'{str(page)}/var/'f'{str(var)}'f'{url_th}')
        elif((model=='pressrelease')|(model=='publication')):
            res = requests.get('https://webapi.bps.go.id/v1/api/list/model/'+model+'/perpage/100000/lang/'+lang+'/domain/'+domain+'/key/'+key+'/keyword/'+keyword+'/page/'+str(page)+
                            (('/month/'+str(month)) if month != '' else '')+
                            (('/year/'+str(year)) if year != '' else ''))
        else:
            res = requests.get(f'{BASE_URL}api/list/model/'f'{model}/perpage/100000/lang/'f'{lang}/domain/'f'{domain}/key/'f'{self.TOKEN}/keyword/'f'{keyword}/page/'f'{str(page)}')
        if(res.status_code!=200):
            warnings.warn("Connection failed")
        else:
            res = res.json()
            if(res['status']!='OK'):
                raise Exception(res['message'])
            return res
        
        

    def __get_view(self,domain,model,lang,idx):
        """
        Based Method view statictable
        :param lang: Language to display data. Default value: ind. Allowed values: "ind", "eng"
        :param domain: Domains that will be displayed variable (see master domain on http://sig.bps.go.id/bridging-kode/index)
        :param model: Type data to display
        :idx : ID static table to show
        """
        res = requests.get(f'{BASE_URL}api/view/model/'f'{model}/lang/'f'{lang}/domain/'f'{domain}/id/'f'{idx}/key/'+self.TOKEN+'/')
        if(res.status_code!=200):
            warnings.warn("Connection failed")
        else:
            res = res.json()
            if(res['status']!='OK'):
                raise Exception(res['message'])
            return res
    
    def __format_list(self,list):
        list['domain'] = list['domain'].map('{0:0>4}'.format)
        return list
        
    def __get_variable(self,domain='0000'):
        """
        Based Method to get all variable of dynamic table
        :param domain: ID domain data
        """
        page = 1
        pages = 1
        var_id = []
        title = []
        sub_id = []
        sub_name = []
        subcsa_id = []
        subcsa_name = []
        def_ = []
        notes = []
        vertical = []
        unit = []
        graph_id = []
        graph_name = []
        df = self.__get_list(lang='ind',domain=domain,model='var',page=page)
        pages = df['data'][0]['pages']
        if(pages>1):
            for page in tqdm(range(1,pages+1)):
                df = self.__get_list(lang='ind',domain=domain,model='var',page=page)
                for item in df['data'][1]:
                    var_id.append(item.get('var_id'))
                    title.append(item.get('title'))
                    sub_id.append(item.get('sub_id'))
                    sub_name.append(item.get('sub_name'))
                    subcsa_id.append(item.get('subcsa_id'))
                    subcsa_name.append(item.get('subcsa_name'))
                    def_.append(item.get('def'))
                    notes.append(item.get('notes'))
                    vertical.append(item.get('vertical'))
                    unit.append(item.get('unit'))
                    graph_id.append(item.get('graph_id'))
                    graph_name.append(item.get('graph_name'))
                df = {
                    'var_id':var_id,
                    'title':title,
                    'sub_id':sub_id,
                    'sub_name':sub_name,
                    'subcsa_id':subcsa_id,
                    'subcsa_name':subcsa_name,
                    'def':def_,
                    'notes':notes,
                    'vertical':vertical,
                    'unit':unit,
                    'graph_id':graph_id,
                    'graph_name':graph_name
                }
        return pd.DataFrame(df) 
    
    def __get_pressRelease(self,domain="0000",year='',month='',keyword=''):
        df = pd.DataFrame({
            'brs_id':[],
            'subj_id':[],
            'subj':[],
            'title':[],
            'abstract':[],
            'rl_date':[],
            'updt_date':[],
            'pdf':[],
            'size':[],
            'slide':[],
            'thumbnail':[]
        })
        res = self.__get_list(domain=domain,model='pressrelease',keyword=keyword,year=year,month=month)
        if(res['data']==''):
            print(res)
            return df
        for item in res['data'][1]:
            df = pd.concat([df, pd.DataFrame({
                'brs_id':[item.get('brs_id')],
                'subj_id':[item.get('subj_id')],
                'subj':[item.get('subj')],
                'title':[item.get('title')],
                'abstract':[item.get('abstract')],
                'rl_date':[item.get('rl_date')],
                'updt_date':[item.get('updt_date')],
                'pdf':[item.get('pdf')],
                'size':[item.get('size')],
                'slide':[item.get('slide')],
                'thumbnail':[item.get('thumbnail')]
            })], axis=0, ignore_index=True)
        pages = res['data'][0]['pages']
        if(res['data'][0]['total']<2):
            print(res)
        if(pages>1):
            for i in tqdm(range(2,pages)):
                res = self.__get_list(domain=domain,model='pressrelease',keyword=keyword,year=year,month=month,page=i)
                if(res['data']==''):
                    break
                for item in res['data'][1]:
                    df = pd.concat([df, pd.DataFrame({
                        'brs_id':[item.get('brs_id')],
                        'subj_id':[item.get('subj_id')],
                        'subj':[item.get('subj')],
                        'title':[item.get('title')],
                        'abstract':[item.get('abstract')],
                        'rl_date':[item.get('rl_date')],
                        'updt_date':[item.get('updt_date')],
                        'pdf':[item.get('pdf')],
                        'size':[item.get('size')],
                        'slide':[item.get('slide')],
                        'thumbnail':[item.get('thumbnail')]
                    })], axis=0, ignore_index=True)
        return df
    
    def __get_publication(self,domain="0000",year='',month='',keyword=''):
        df = pd.DataFrame({
            'pub_id':[],
            'title':[],
            'abstract':[],
            'issn':[],
            'sch_date':[],
            'rl_date':[],
            'updt_date':[],
            'cover':[],
            'pdf':[],
            'size':[]
        })
        res = self.__get_list(domain=domain,model='pressrelease',keyword=keyword,year=year,month=month)
        if(res['data']==''):
            return df
        for item in res['data'][1]:
            df = pd.concat([df, pd.DataFrame({
                'pub_id':[item.get('pub_id')],
                'title':[item.get('title')],
                'abstract':[item.get('abstract')],
                'issn':[item.get('issn')],
                'sch_date':[item.get('sch_date')],
                'rl_date':[item.get('rl_date')],
                'updt_date':[item.get('updt_date')],
                'cover':[item.get('cover')],
                'pdf':[item.get('pdf')],
                'size':[item.get('size')]
            })], axis=0, ignore_index=True)
        pages = res['data'][0]['pages']
        if(pages>1):
            for i in tqdm(range(2,pages)):
                res = self.__get_list(domain=domain,model='pressrelease',keyword=keyword,year=year,month=month,page=i)
                if(res['data']==''):
                    break
                for item in res['data'][1]:
                    df = pd.concat([df, pd.DataFrame({
                        'pub_id':[item.get('pub_id')],
                        'title':[item.get('title')],
                        'abstract':[item.get('abstract')],
                        'issn':[item.get('issn')],
                        'sch_date':[item.get('sch_date')],
                        'rl_date':[item.get('rl_date')],
                        'updt_date':[item.get('updt_date')],
                        'cover':[item.get('cover')],
                        'pdf':[item.get('pdf')],
                        'size':[item.get('size')]
                    })], axis=0, ignore_index=True)
        return df
    
    def __get_statictable(self,domain='0000',keyword=''):
        """
        Based Method to get all static table
        :param domain: ID domain data
        :param keyword: keyword to search specific table
        """
        df = pd.DataFrame({
            'table_id':[],
            'title':[],
            'subj_id':[],
            'subj':[],
            'updt_date':[],
            'size':[],
            'excel':[]
        })
        res = self.__get_list(domain=domain,model='statictable',keyword=keyword)
        if(res['data']==''):
            return df
        for item in res['data'][1]:
            df = pd.concat([df, pd.DataFrame({
                'table_id':[item.get('table_id')],
                'title':[item.get('title')],
                'subj_id':[item.get('subj_id')],
                'subj':[item.get('subj')],
                'updt_date':[item.get('updt_date')],
                'size':[item.get('size')],
                'excel':[item.get('excel')]
            })], axis=0, ignore_index=True)
        pages = res['data'][0]['pages']
        if(pages>1):
            for i in tqdm(range(2,pages)):
                res = self.__get_list(domain=domain,model='statictable',keyword=keyword,page=i)
                if(res['data']==''):
                    break
                for item in res['data'][1]:
                    df = pd.concat([df, pd.DataFrame({
                        'table_id':[item.get('table_id')],
                        'title':[item.get('title')],
                        'subj_id':[item.get('subj_id')],
                        'subj':[item.get('subj')],
                        'updt_date':[item.get('updt_date')],
                        'size':[item.get('size')],
                        'excel':[item.get('excel')]
                    })], axis=0, ignore_index=True)
        return df
    
    def list_statictable(self, all=False, domain=[],latest=False):
        """
        Method to get all static table
        :param domain: array of ID domain data
        :param all: get all data from whole domain or not
        :param latest:get last data from webapi
        """
        if(not latest):
            allStaticTable = pd.read_csv('https://gist.githubusercontent.com/isandyawan/31c29bd92039c4ff7b736826a7065028/raw/allStaticTable.csv',sep="|")
            if(not all):
                domain = [int(numeric_string) for numeric_string in domain]
                allStaticTable.loc[allStaticTable['domain'].isin(domain)]
        else: 
            if(all):
                warnings.warn("It will take around 2 hour")
                domain = self.list_domain()
                domain = domain['domain_id'].values
            allStaticTable = []
            index = 0
            for row in domain:
                res = self.__get_statictable(domain=row)
                res['domain'] = row
                if(index==0):
                    allStaticTable = res
                else:
                    allStaticTable = pd.concat([allStaticTable,res])
                index += 1
        allStaticTable = self.__format_list(allStaticTable)
        return allStaticTable
    
    def list_dynamictable(self, all=False, domain=[],latest=False):
        """
        Method to get all dynamic table
        :param domain: array of ID domain data
        :param all: get all data from whole domain or not
        :param latest:get last data from webapi
        """
        if(not latest):
            allVariable = pd.read_csv('https://gist.githubusercontent.com/isandyawan/4d3efaeea4608c11b1e22b8a51fd0e4d/raw/allVariable.csv',sep="|")
            if(not all):
                domain = [int(numeric_string) for numeric_string in domain]
                allVariable.loc[allVariable['domain'].isin(domain)]
        else: 
            index = 0
            allVariable = []
            if(all):
                warnings.warn("It will take around 2 hour")
                domain = self.list_domain()
                domain = domain['domain_id'].values
            for row in domain:
                res = self.__get_variable(domain=row)
                res['domain'] = row
                if(index==0):
                    allVariable = res
                else:
                    allVariable = pd.concat([allVariable,res])
                index += 1
        allVariable = self.__format_list(allVariable)
        return allVariable
    
    def list_pressrelease(self, all=True, domain=[], month="",year="",latest=False):
        """
        Method to get all press release
        :param domain: array of ID domain data
        :param all: get all data from whole domain or not
        :param latest:get last data from webapi
        """
        if(not latest):
            allPressRelease = pd.read_csv('https://gist.githubusercontent.com/isandyawan/4e67a8cf452838e914187e3597bf70c4/raw/allPressRelease.csv',sep="|", index_col=[0])
            if(not all):
                domain = [int(numeric_string) for numeric_string in domain]
                allPressRelease.loc[allPressRelease['domain'].isin(domain)]
                if((month!="") & (year !="")):
                    allPressRelease = allPressRelease.loc[allPressRelease['rl_date'].str.contains(year+'-'+'{0:0>2}'.format(month))]
        else: 
            if(all):
                warnings.warn("It will take around 4 hour")
                domain = self.list_domain()
                domain = domain['domain_id'].values
            allPressRelease = []
            index = 0
            for row in domain:
                res = self.__get_pressRelease(domain=row,month=month,year=year)
                res['domain'] = row
                if(index==0):
                    allPressRelease = res
                else:
                    allPressRelease = pd.concat([allPressRelease,res])
                index += 1
        allPressRelease = self.__format_list(allPressRelease)
        return allPressRelease
    
    def list_publication(self, all=True, domain=[], month="",year="",latest=False):
        """
        Method to get all publication
        :param domain: array of ID domain data
        :param all: get all data from whole domain or not
        :param latest:get last data from webapi
        """
        if(not latest):
            allPublication = pd.read_csv('https://gist.githubusercontent.com/isandyawan/31b48670d76a199bc88fba3ec3c0672f/raw/allPublication.csv',sep="|", index_col=[0])
            if(not all):
                domain = [int(numeric_string) for numeric_string in domain]
                allPublication = allPublication.loc[allPublication['domain'].isin(domain)]
                if((month!="") & (year !="")):
                    allPublication = allPublication.loc[allPublication['rl_date'].str.contains(year+'-'+'{0:0>2}'.format(month))]
        else: 
            if(all):
                warnings.warn("It will take around 4 hour")
                domain = self.list_domain()
                domain = domain['domain_id'].values
            allPublication = []
            index = 0
            for row in domain:
                res = self.__get_publication(domain=row,month=month,year=year)
                res['domain'] = row
                if(index==0):
                    allPublication = res
                else:
                    allPublication = pd.concat([allPublication,res])
                index += 1
        allPublication = self.__format_list(allPublication)
        return allPublication

    def list_domain(self):
        """
        Method to get all domain ID in level country till city
        """
        res = requests.get(f'{BASE_URL}api/domain/type/all/key/'f'{self.TOKEN}/')
        if(res.status_code!=200):
            warnings.warn("Connection failed")
            return None
        else:
            res = res.json()
            if(res['status']!='OK'):
                raise Exception(res['message'])
            domain_id = []
            domain_name = []
            domain_url = []
            for item in res['data'][1]:
                domain_id.append(item['domain_id'])
                domain_name.append(item['domain_name'])
                domain_url.append(item['domain_url'])
            df = {
                'domain_id':domain_id,
                'domain_name':domain_name,
                'domain_url':domain_url
            }
            result = pd.DataFrame(df)
            result['level'] = 'kota/kabupaten'
            result.loc[result['domain_id'].str.match('^.*00$'),'level'] = 'provinsi'
            result.loc[result['domain_id'].str.match('0000'),'level'] = 'nasional'
            return result
        
    def view_statictable(self,domain,table_id,lang='ind'):
        """
        Method to view one static table
        :param domain: Domains that will be displayed variable (see master domain on http://sig.bps.go.id/bridging-kode/index)
        :param table_id: ID static table
        :param lang: Language to display data. Default value: ind. Allowed values: "ind", "eng"
        """
        res = self.__get_view(domain,'statictable',lang,table_id)
        res_clean = html.unescape(res['data']['table'])
        df = pd.read_html(res_clean)[0]
        return df
    
    def view_(self,domain,table_id,lang='ind'):
        """
        Method to view one static table
        :param domain: Domains that will be displayed variable (see master domain on http://sig.bps.go.id/bridging-kode/index)
        :param table_id: ID static table
        :param lang: Language to display data. Default value: ind. Allowed values: "ind", "eng"
        """
        res = self.__get_view(domain,'statictable',lang,table_id)
        res_clean = html.unescape(res['data']['table'])
        df = pd.read_html(res_clean)[0]
        return df

    def view_pressrelease(self,domain,id):
        res = self.__get_view(domain=domain,model='pressrelease',idx=id,lang='ind')
        return Material(res['data'])
    
    def view_publication(self,domain,id):
        res = self.__get_view(domain=domain,model='publication',idx=id,lang='ind')
        return Material(res['data'])
        
    def view_dynamictable(self,domain,var,th=''):
        """
        Method to view one dynamic table
        :param var: Variable ID selected to display data
        :param th: Period data ID selected to display data
        """
        res = self.__get_list(lang = 'ind',domain=domain,model='data',page=1,var=var,th=th)
        if(res['data']==''):
            return None
        res['datacontent'].values()
        datacontent = pd.DataFrame({
            'key':res['datacontent'].keys(),
            'value':res['datacontent'].values()
        })
        
        datacontent = datacontent.sort_values('key',ignore_index=True)

        vervar = pd.DataFrame(list(map(lambda x: [x['val'],x['label']], res['vervar'])),columns=['id_var','variable'])
        vervar = vervar.sort_values('id_var',ignore_index=True)

        turvar = pd.DataFrame(list(map(lambda x: [x['val'],x['label']], res['turvar'])),columns=['id_tur_var','turunan variable'])
        turvar = turvar.sort_values('id_tur_var',ignore_index=True)
        
        result = vervar.merge(turvar,how='cross')
        
        tahun = pd.DataFrame(list(map(lambda x: [x['val'],x['label']], res['tahun'])),columns=['val','label'])
        tahun = tahun.sort_values('val',ignore_index=True)
        
        for index, row in tahun.iterrows():
            result[row['label']]=''
            for index_result, row_result in result.iterrows():
                cell = datacontent.loc[datacontent['key'].str.match('^'+str(result.loc[index_result,'id_var'])+str(var)+str(result.loc[index_result,'id_tur_var'])+str(row['val'])),'value']
                if(len(cell)==0):
                    continue
                result.loc[index_result,str(row['label'])] = cell.reset_index(drop=True)[0]
        return result