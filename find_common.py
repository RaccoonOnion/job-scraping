def find_common_fields(dict1, dict2, prefix=''):
    common_fields = []

    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    shared_keys = keys1.intersection(keys2)

    for key in shared_keys:
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            # Recurse into nested dictionaries
            common_fields.extend(find_common_fields(dict1[key], dict2[key], full_key))
        else:
            # If both are not dicts, consider them a common field
            common_fields.append(full_key)

    return common_fields

# Example usage:
import json

# Replace these with your actual JSON objects
json1 =    {
     "data": {
       "slug": "25736-604612",
       "language": "en-us",
       "languages": ["en-us"],
       "req_id": "403466BR",
       "title": "Package Handler- Switcher FT",
       "description": "Job Summary Responsible for the movement of trailers to and from the unload / load doors and throughout the yard. May also be responsible for the physical loading, unloading and/or sorting of packages by hand, including lifting, pushing, pulling, carrying and placing, in a safe and efficient manner. Essential Functions • Performs trailer switches defined as hooking and moving a parked trailer from the yard to a load/unload door or hooking and moving a trailer from a door to the yard. • Communicates with management and/or central control to coordinate trailer movements in the yard. • Documents trailer moves using the Yard Management System (where available) or switcher cards. • Performs pre- and post-trip inspections on switcher equipment. • Understands and demonstrates effective yard switching safety processes and procedures. In addition to the above essential functions, Switchers may also be required to perform Package Handler essential functions as follows: • Utilizes “hand-to-surface” methods for all package handling. • Loads and unloads packages onto or from delivery vehicles, trailers, conveyor system carts and load gratings. • Lifts, carries, pushes and pulls packages on a continuous and repetitive basis for approximate shifts of two to four hours. • Determines the appropriate conveyor system by scanning packages, reading labels and charts, verifying numbers and memorizing information and sorts packages accordingly. Minimum Education None Minimum Experience No experience required; six (6) months of experience as a package handler or switching/CDL operator experience preferred. Required Skills, Abilities and / or Licensure •Must have a valid driver’s license and maintain a Department of Transportation (DOT) file. •Ability to understand and follow instruction regarding work duties and safety methods. • Ability to discern numbers and information in order to sort packages correctly. •Ability to use basic tools and equipment such as skate wheel rollers, dock carts, hand-held scanners, chutes and unloading devices. •Strong communication and interpersonal skills; ability to work well in a fast-paced team environment.Address: 1101 E Cleveland Road City: Hutchins State: Texas Zip Code: 75141 Domicile Location: FXG-US/USA/P753/Dallas - Hub Auto req ID: 403466BR Position Type: Full time Employee Type: Non-Exempt EEO Statement FedEx Ground is an equal opportunity / affirmative action employer (Minorities/Females/Disability/Veterans) committed to a diverse workforceSearch Engine Description: Handler/Dockworker Operations Transportation Services Warehouse & Distribution",
       "street_address": "1101 E Cleveland Road",
       "city": "Hutchins",
       "state": "Texas",
       "country_code": "US",
       "postal_code": "75141",
       "location_type": "LAT_LNG",
       "latitude": 32.6574419,
       "longitude": -96.7055958,
       "categories": [
         { "name": "Handler/Dockworker" },
         { "name": "Operations" },
         { "name": "Transportation Services" },
         { "name": "Warehouse & Distribution" }
       ],
       "tags": ["groundcareers"],
       "tags5": ["FedEx Ground"],
       "tags6": ["Non-Exempt"],
       "brand": "FedEx Ground",
       "promotion_value": 0,
       "salary_currency": "USD",
       "salary_value": 0,
       "salary_min_value": 0,
       "salary_max_value": 0,
       "benefits": [
         "VISION",
         "SICK_DAYS",
         "VACATION",
         "DENTAL",
         "PARENTAL_LEAVE",
         "CHILD_CARE",
         "MEDICAL"
       ],
       "employment_type": "FULL_TIME",
       "hiring_organization": "FedEx Ground",
       "source": "ground-careers",
       "apply_url": "https://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?PageType=JobDetails&partnerid=25736&siteid=5029&jobid=604612",
       "internal": False,
       "searchable": True,
       "applyable": True,
       "li_easy_applyable": True,
       "ats_code": "fedexground-prod-kenexa",
       "meta_data": {
         "ats": "kenexa",
         "ats_instance": "Ground",
         "client_code": "fedex",
         "district_description": "Lone Star District",
         "domicile_location": "FXG-US/USA/P753/Dallas - Hub",
         "domicile_location_name": "Dallas - Hub",
         "extensions": "KenexaResponsive",
         "flow_config_name": "1026",
         "gqid": "1026",
         "import_source": "kenexa-job-importer",
         "locale_id": "1033",
         "login": "kenexa",
         "login_url": "https://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?PageType=JobDetails&partnerid=25736&siteid=5029&jobid=604612",
         "openingjobs": {},
         "partner_id": 25736,
         "question_sets": [
           { "name": "fedexkenexa_registration_en_us", "ordinal": 0 },
           { "name": "fedexground_1026_en_us", "ordinal": 2 }
         ],
         "questionservice": { "id": "28946776" },
         "region_description": "Gulf Region",
         "site_id": "5029",
         "source_tracking": {
           "options": { "login_url": True, "url_parameter": "Codes" },
           "type": "url_parameter"
         },
         "use_poltergeist": False,
         "googlejobs": {
           "companyName": "projects/helpful-passage-853/tenants/cb22eb5b-7e00-0000-0000-007edad744d3/companies/6c91e1ea-b6bf-4674-9332-0f6e63a2d98f",
           "jobName": "projects/helpful-passage-853/tenants/cb22eb5b-7e00-0000-0000-007edad744d3/jobs/101356581498561222",
           "jobHash": "e245fa50c753492a57135d9fb2599086",
           "derivedInfo": {
             "jobCategories": [
               "MANUFACTURING_AND_WAREHOUSE",
               "TRANSPORTATION_AND_LOGISTICS"
             ],
             "locations": [
               {
                 "latLng": {
                   "latitude": 32.6574419,
                   "longitude": -96.7055958
                 },
                 "locationType": "STREET_ADDRESS",
                 "postalAddress": {
                   "addressLines": [
                     "1101 E Cleveland St, Hutchins, TX 75141, USA"
                   ],
                   "administrativeArea": "TX",
                   "languageCode": "",
                   "locality": "Hutchins",
                   "organization": "",
                   "postalCode": "75141",
                   "recipients": [],
                   "regionCode": "US",
                   "revision": 0,
                   "sortingCode": "",
                   "sublocality": ""
                 },
                 "radiusInMiles": 0.00009925704072722659
               }
             ]
           },
           "jobSummary": "Job Summary Responsible for the movement of trailers to and from the unload / load doors and throughout the yard. May also be responsible for the physical loading, unloading and/or sorting of packages by hand, including lifting, pushing, pulling, carrying and placing, in a safe and efficient manner. Essential Functions • Performs trailer switches defined as hooking and moving a parked trailer from the yard to a load/unload door or hooking and moving a trailer from a door to the yard. • Communicates with management and/or central control to coordinate trailer movements in the yard. • Documents trailer moves using the Yard Management System (where available) or switcher cards. • Performs pre- and post-trip inspections on switcher equipment. • Understands and demonstrates effective yard switching safety processes and procedures. In addition to the above essential functions, Switchers may also be required to perform Package Handler essential functions as follows: • Utilizes “hand-to-surface” methods for all package handling. • Loads and unloads packages onto or from delivery vehicles, trailers, conveyor system carts and load gratings. • Lifts, carries, pushes and pulls packages on a continuous and repetitive basis for approximate shifts of two to four hours. • Determines the appropriate conveyor system by scanning packages, reading labels and charts, verifying numbers and memorizing information and sorts packages accordingly. Minimum Education None Minimum Experience No experience required; six (6) months of experience as a package handler or switching/CDL operator experience preferred. Required Skills, Abilities and / or Licensure •Must have a valid driver’s license and maintain a Department of Transportation (DOT) file. •Ability to understand and follow instruction regarding work duties and safety methods. • Ability to discern numbers and information in order to sort packages correctly. •Ability to use basic tools and equipment such as skate wheel rollers, dock carts, hand-held scanners, chutes and unloading devices. •Strong communication and interpersonal skills; ability to work well in a fast-paced team environment.Address: 1101 E Cleveland Road City: Hutchins State: Texas Zip Code: 75141 Domicile Location: FXG-US/USA/P753/Dallas - Hub Auto req ID: 403466BR Position Type: Full time Employee Type: Non-Exempt EEO Statement FedEx Ground is an equal opportunity / affirmative action employer (Minorities/Females/Disability/Veterans) committed to a diverse workforceSearch Engine Description: Handler/Dockworker Operations Transportation Services Warehouse & Distribution",
           "jobTitleSnippet": "",
           "searchTextSnippet": ""
         },
         "canonical_url": "https://careers.fedex.com/jobs/25736-604612?lang=en-us",
         "last_mod": "2024-02-02T06:06:02+0000",
         "gdpr": False
       },
       "update_date": "2024-02-02T06:06:02+0000",
       "create_date": "2024-02-02T06:06:00+0000",
       "category": [
         " Handler/Dockworker",
         " Operations",
         " Transportation Services",
         " Warehouse & Distribution"
       ],
       "full_location": "Hutchins, Texas",
       "short_location": "Hutchins, Texas"
     }
   }

json2 =    {
     "data": {
       "slug": "200002WM",
       "language": "en-us",
       "languages": ["en-us", "es-mx"],
       "req_id": "200002WM",
       "title": "Hub Order Puller",
       "description": "Position Summary The Hub Order Puller ensures maximum productivity, stocks merchandise, looks up and pulls parts, and remains compliant with company procedures in accordance to AutoZone’s expectation by Living the Pledge everyday. Position Responsibilities Ensures store tasks are completed in a timely manner on assigned shift Maintains Hub appearance and merchandising standards Maintains a safe working environment including PPE (Personal Protective Equipment) Follows company policies and loss prevention procedures Reviews condition of hard parts and feeder area and ensure there are no safety concerns Process and verify orders are pulled, staged, and accurate Ensures returns from stores during route deliveries are restocked appropriately and in a timely manner Maintains quality control accuracy and fill rate Goal of 99.0%. Utilizes ZNET to help customers locate merchandise or find suitable alternatives Ensures all incoming returns are put up in a timely Position Requirements High School Diploma or equivalent Basic knowledge of automotive parts is required Excellent communication and decision making skills Ability to lift, load, and deliver merchandise Ability to work a flexible schedule to meet the business needs, including holidays, evenings and weekend shifts",
       "location_name": "USA #0226",
       "street_address": "130 GREEN SPRINGS HWY",
       "city": "Birmingham",
       "state": "Alabama",
       "country": "United States",
       "country_code": "US",
       "postal_code": "35209",
       "location_type": "LAT_LNG",
       "latitude": 33.4680988,
       "longitude": -86.8258575,
       "categories": [{ "name": "Stores - Hub" }],
       "tags": ["Stores"],
       "brand": "AutoZone-US",
       "promotion_value": 0,
       "apply_url": "https://autozone.taleo.net/careersection/AZ_External/jobapply.ftl?job=200002WM&lang=en",
       "internal": False,
       "searchable": True,
       "applyable": True,
       "li_easy_applyable": False,
       "ats_code": "autozone-prod-taleo",
       "meta_data": {
         "ats": "taleo",
         "ats_id": "200002WM",
         "ats_instance": "autozone-prod-taleo",
         "career_sections": ["AZ_External", "AZ_Stores"],
         "client_code": "autozone",
         "import_source": "taleo-integration",
         "redirectOnApply": True,
         "googlejobs": {
           "companyName": "projects/helpful-passage-853/tenants/cb22eb5b-7e00-0000-0000-007edad744d3/companies/d77f4b6c-c67c-4826-9d18-491e97843edf",
           "jobName": "projects/helpful-passage-853/tenants/cb22eb5b-7e00-0000-0000-007edad744d3/jobs/86052164587135686",
           "jobHash": "9d8b68d9c25d06f32be210fa30ba8788",
           "derivedInfo": {
             "jobCategories": [
               "SALES_AND_RETAIL",
               "MANUFACTURING_AND_WAREHOUSE"
             ],
             "locations": [
               {
                 "latLng": {
                   "latitude": 33.4680988,
                   "longitude": -86.8258575
                 },
                 "locationType": "STREET_ADDRESS",
                 "postalAddress": {
                   "addressLines": [
                     "130 Green Springs Hwy, Birmingham, AL 35209, USA"
                   ],
                   "administrativeArea": "AL",
                   "languageCode": "",
                   "locality": "Birmingham",
                   "organization": "",
                   "postalCode": "35209",
                   "recipients": [],
                   "regionCode": "US",
                   "revision": 0,
                   "sortingCode": "",
                   "sublocality": ""
                 },
                 "radiusInMiles": 0.00008265742998509635
               }
             ]
           },
           "jobSummary": "Position Summary The Hub Order Puller ensures maximum productivity, stocks merchandise, looks up and pulls parts, and remains compliant with company procedures in accordance to AutoZone’s expectation by Living the Pledge everyday. Position Responsibilities Ensures store tasks are completed in a timely manner on assigned shift Maintains Hub appearance and merchandising standards Maintains a safe working environment including PPE (Personal Protective Equipment) Follows company policies and loss prevention procedures Reviews condition of hard parts and feeder area and ensure there are no safety concerns Process and verify orders are pulled, staged, and accurate Ensures returns from stores during route deliveries are restocked appropriately and in a timely manner Maintains quality control accuracy and fill rate Goal of 99.0%. Utilizes ZNET to help customers locate merchandise or find suitable alternatives Ensures all incoming returns are put up in a timely Position Requirements High School Diploma or equivalent Basic knowledge of automotive parts is required Excellent communication and decision making skills Ability to lift, load, and deliver merchandise Ability to work a flexible schedule to meet the business needs, including holidays, evenings and weekend shifts",
           "jobTitleSnippet": "",
           "searchTextSnippet": ""
         },
         "canonical_url": "https://careers.autozone.com/jobs/200002WM?lang=en-us",
         "last_mod": "2024-02-02T07:04:18+0000",
         "gdpr": False
       },
       "update_date": "2024-02-02T07:04:18+0000",
       "create_date": "2021-07-24T22:17:49+0000",
       "category": [" Stores - Hub"],
       "full_location": "Birmingham, Alabama",
       "short_location": "Birmingham, Alabama"
     }
   }



common = find_common_fields(json1["data"], json2["data"])
print("Common fields:")
for field in common:
    print(field)
