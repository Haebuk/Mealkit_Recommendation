from market_kurly.kurly_scrapping import Kurly_Scrapping

try:
    with Kurly_Scrapping() as kurly:
        kurly.land_first_page()
        product_list = kurly.get_product_list()
        print(f'product list length: {len(product_list)}')
        for iter in range(len(product_list)):
            print('------' + str(iter+1) + '------')
            kurly.click_product(iter)    
            kurly.refresh()
            product_url = kurly.get_product_url()
            product_name = kurly.get_product_name()
            kurly.land_first_page()

            if iter == 5:
                break

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise