# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import re

    code = '''=== while ===
     1. 중첩된 comment 금지
      1. 중첩된 comment 금지
  comment를 포함하는 부분을 주석처리하지 않는다. 여러줄 코드를 주석처리 할 경우 if 전처리기를 사용한다.
 {{{
 /*
if (fcntl(sock, F_SETFL, O_NDELAY) < 0) {
	/* error occur */   <---- 컴파일 오류 발생
	return -1;
}
*/
}}}
'''
    code = '''
    ==== example ====
 {{{#!vim python
if __name__ == '__main__':
    from win32com.client import Dispatch 
    calc_fx = Dispatch('fngFX.fx1')
    opt_param = Fngfx()

    opt_param['bizday']=1
    opt_param['assetcnt']=1
    opt_param['PrType']=2
    opt_param['udflag']=[0] * 4
    opt_param['sval']=[77.819999999999993, 14.344641480339245, 1116.3]
    opt_param['bsval']=[83.52] * 1
    opt_param['dxval']=[83.52] * 4
    opt_param['prev']=[0.0] * 1
    }}}
    fdsa
    '''

    special = ''.join(['\\' + x for x in '+-*/= .,;:!?#&$%@|^(){}[]~<>\''])
    inner_code = '[ ]*[\{]{3}([#!a-z ]*)\n([\w\s가-힣' + special + ']*)[\}]{3}'
    # inner_code = '(\[)(http[s]?://[\w\-./%#가-힣]+) ([a-zA-Z0-9.가-힣 \+\/]+)(\])'
    inner_code = '[ ]*[\{]{3}([#!a-z ]*)\n([\w\s가-힣' + special + ']*)[\}]{3}'

    matchs = re.findall(inner_code, code)

    if (len(matchs) > 0):
        print(matchs[0][1])
