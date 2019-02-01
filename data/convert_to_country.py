# This is to obtain country code and continent info for countries
# Source: http://data.unhcr.org/wiki/index.php/Get-countries-list.html
import pandas as pd
clist = [

    {
        "name_en": "Afghanistan",
        "country_code": "AFG",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Albania",
        "country_code": "ALB",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Algeria",
        "country_code": "ALG",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Andorra",
        "country_code": "AND",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Angola",
        "country_code": "ANG",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Anguilla",
        "country_code": "AIA",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Antigua and Barbuda",
        "country_code": "ANT",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Argentina",
        "country_code": "ARG",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Armenia",
        "country_code": "ARM",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Aruba",
        "country_code": "ABW",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Australia",
        "country_code": "AUL",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Austria",
        "country_code": "AUS",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Azerbaijan",
        "country_code": "AZE",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Bahamas",
        "country_code": "BHS",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Bahrain",
        "country_code": "BAH",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Bangladesh",
        "country_code": "BGD",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Barbados",
        "country_code": "BAR",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Belarus",
        "country_code": "BLR",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Belgium",
        "country_code": "BEL",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Belize",
        "country_code": "BZE",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Benin",
        "country_code": "BEN",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Bermuda",
        "country_code": "BER",
        "region_code": "021",
        "region_code_en": "Northern America"
    },
    {
        "name_en": "Bhutan",
        "country_code": "BHU",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Bolivia (Plurinational State of)",
        "country_code": "BOL",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Bonaire, Sint Eustatius and Saba",
        "country_code": "BES",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Bosnia and Herzegovina",
        "country_code": "BSN",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Botswana",
        "country_code": "BOT",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Brazil",
        "country_code": "BRA",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "British Virgin Islands",
        "country_code": "BVI",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Brunei Darussalam",
        "country_code": "BRU",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Bulgaria",
        "country_code": "BUL",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Burkina Faso",
        "country_code": "BKF",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Burundi",
        "country_code": "BDI",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Cambodia",
        "country_code": "CAM",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Cameroon",
        "country_code": "CMR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Canada",
        "country_code": "CAN",
        "region_code": "021",
        "region_code_en": "Northern America"
    },
    {
        "name_en": "Cape Verde",
        "country_code": "CVI",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Cayman Islands",
        "country_code": "CAY",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Central African Republic",
        "country_code": "CAR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Chad",
        "country_code": "CHD",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Chile",
        "country_code": "CHL",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "China",
        "country_code": "CHI",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Colombia",
        "country_code": "COL",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Comoros",
        "country_code": "COI",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Congo",
        "country_code": "COB",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Cook Islands",
        "country_code": "COK",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Costa Rica",
        "country_code": "COS",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Croatia",
        "country_code": "HRV",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Cuba",
        "country_code": "CUB",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Curacao",
        "country_code": "CUW",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Cyprus",
        "country_code": "CYP",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Czech Republic",
        "country_code": "CZE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Côte d'Ivoire",
        "country_code": "ICO",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Democratic People's Republic of Korea",
        "country_code": "KRN",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Democratic Republic of the Congo",
        "country_code": "COD",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Denmark",
        "country_code": "DEN",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Djibouti",
        "country_code": "DJB",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Dominica",
        "country_code": "DMA",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Dominican Republic",
        "country_code": "DOM",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Ecuador",
        "country_code": "ECU",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Egypt",
        "country_code": "ARE",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "El Salvador",
        "country_code": "SAL",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Equatorial Guinea",
        "country_code": "EGU",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Eritrea",
        "country_code": "ERT",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Estonia",
        "country_code": "EST",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Ethiopia",
        "country_code": "ETH",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Faeroe Islands",
        "country_code": "FRO",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Federal Republic of Yugoslavia",
        "country_code": "YUG",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Fiji",
        "country_code": "FIJ",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Finland",
        "country_code": "FIN",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "France",
        "country_code": "FRA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "French Guiana",
        "country_code": "FGU",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "French Polynesia",
        "country_code": "FPO",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Gabon",
        "country_code": "GAB",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Gambia",
        "country_code": "GAM",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Georgia",
        "country_code": "GEO",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Germany",
        "country_code": "GFR",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Ghana",
        "country_code": "GHA",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Gibraltar",
        "country_code": "GIB",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Greece",
        "country_code": "GRE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Greenland",
        "country_code": "GRL",
        "region_code": "021",
        "region_code_en": "Northern America"
    },
    {
        "name_en": "Grenada",
        "country_code": "GRN",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Guatemala",
        "country_code": "GUA",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Guinea",
        "country_code": "GUI",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Guinea-Bissau",
        "country_code": "GNB",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Guyana",
        "country_code": "GUY",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Haiti",
        "country_code": "HAI",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Holy See",
        "country_code": "VAT",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Honduras",
        "country_code": "HON",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Hong Kong SAR, China",
        "country_code": "HKG",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Hungary",
        "country_code": "HUN",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Iceland",
        "country_code": "ICE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "India",
        "country_code": "IND",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Indonesia",
        "country_code": "INS",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Iran (Islamic Republic of)",
        "country_code": "IRN",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Iraq",
        "country_code": "IRQ",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Ireland",
        "country_code": "IRE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Israel",
        "country_code": "ISR",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Italy",
        "country_code": "ITA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Jamaica",
        "country_code": "JAM",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Japan",
        "country_code": "JPN",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Jordan",
        "country_code": "JOR",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Kazakhstan",
        "country_code": "KAZ",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Kenya",
        "country_code": "KEN",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Kiribati",
        "country_code": "KIR",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Kosovo (S/RES/1244 (1999))",
        "country_code": "KOS",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Kuwait",
        "country_code": "KUW",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Kyrgyzstan",
        "country_code": "KGZ",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Lao People's Democratic Republic",
        "country_code": "LAO",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Latvia",
        "country_code": "LVA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Lebanon",
        "country_code": "LEB",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Lesotho",
        "country_code": "LES",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Liberia",
        "country_code": "LBR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Libya",
        "country_code": "LBY",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Libyan Arab Jamahiriya",
        "country_code": "LBY",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Liechtenstein",
        "country_code": "LIE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Lithuania",
        "country_code": "LTU",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Luxembourg",
        "country_code": "LUX",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Macao SAR, China",
        "country_code": "MAC",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Madagascar",
        "country_code": "MAD",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Malawi",
        "country_code": "MLW",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Malaysia",
        "country_code": "MLS",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Maldives",
        "country_code": "MDV",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Mali",
        "country_code": "MLI",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Malta",
        "country_code": "MTA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Marshall Islands",
        "country_code": "MHL",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Martinique",
        "country_code": "MAR",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Mauritania",
        "country_code": "MAU",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Mauritius",
        "country_code": "MTS",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Mexico",
        "country_code": "MEX",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Micronesia (Federated States of)",
        "country_code": "FSM",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Monaco",
        "country_code": "MCO",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Mongolia",
        "country_code": "MNG",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Montenegro",
        "country_code": "MNE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Montserrat",
        "country_code": "MSR",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Morocco",
        "country_code": "MOR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Mozambique",
        "country_code": "MOZ",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Myanmar",
        "country_code": "MYA",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Namibia",
        "country_code": "NAM",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Nauru",
        "country_code": "NRU",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Nepal",
        "country_code": "NEP",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Netherlands",
        "country_code": "NET",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "New Caledonia",
        "country_code": "FNC",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "New Zealand",
        "country_code": "NZL",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Nicaragua",
        "country_code": "NIC",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Niger",
        "country_code": "NGR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Nigeria",
        "country_code": "NIG",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Niue",
        "country_code": "NIU",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Norway",
        "country_code": "NOR",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Oman",
        "country_code": "OMN",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Pakistan",
        "country_code": "PAK",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Palau",
        "country_code": "PLW",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Palestinian Territory, Occupied",
        "country_code": "GAZ",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Panama",
        "country_code": "PAN",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Papua New Guinea",
        "country_code": "PNG",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Paraguay",
        "country_code": "PAR",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Peru",
        "country_code": "PER",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Philippines",
        "country_code": "PHI",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Pitcairn",
        "country_code": "PCN",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Poland",
        "country_code": "POL",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Portugal",
        "country_code": "POR",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Puerto Rico",
        "country_code": "PUE",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Qatar",
        "country_code": "QAT",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Republic of Korea",
        "country_code": "KOR",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Republic of Moldova",
        "country_code": "MDA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Romania",
        "country_code": "ROM",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Russian Federation",
        "country_code": "RUS",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Rwanda",
        "country_code": "RWA",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Saint Kitts and Nevis",
        "country_code": "STK",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Saint Lucia",
        "country_code": "LCA",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Saint Vincent and the Grenadines",
        "country_code": "VCT",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Samoa",
        "country_code": "WES",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "San Marino",
        "country_code": "SMA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Sao Tome and Principe",
        "country_code": "STP",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Saudi Arabia",
        "country_code": "SAU",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Senegal",
        "country_code": "SEN",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Serbia (and Kosovo: S/RES/1244 (1999))",
        "country_code": "SRB",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Serbia and Montenegro",
        "country_code": "YUG",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Seychelles",
        "country_code": "SEY",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Sierra Leone",
        "country_code": "SLE",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Singapore",
        "country_code": "SIN",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Sint Maarten (Dutch part)",
        "country_code": "SXM",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Slovakia",
        "country_code": "SVK",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Slovenia",
        "country_code": "SVN",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Solomon Islands",
        "country_code": "SOL",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Somalia",
        "country_code": "SOM",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "South Africa",
        "country_code": "RSA",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "South Sudan",
        "country_code": "SSD",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Spain",
        "country_code": "SPA",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Sri Lanka",
        "country_code": "LKA",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "State of Palestine",
        "country_code": "GAZ",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Sudan",
        "country_code": "SUD",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Sudan",
        "country_code": "SUD",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Suriname",
        "country_code": "SUR",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Swaziland",
        "country_code": "SWA",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Sweden",
        "country_code": "SWE",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Switzerland",
        "country_code": "SWI",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Syrian Arab Republic",
        "country_code": "SYR",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Tajikistan",
        "country_code": "TJK",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Thailand",
        "country_code": "THA",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "The former Yugoslav Republic of Macedonia",
        "country_code": "MCD",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "Timor-Leste",
        "country_code": "TMP",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Togo",
        "country_code": "TOG",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Tonga",
        "country_code": "TON",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Trinidad and Tobago",
        "country_code": "TRT",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Tunisia",
        "country_code": "TUN",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Turkey",
        "country_code": "TUR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Turkmenistan",
        "country_code": "TKM",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Turks and Caicos Islands",
        "country_code": "TCI",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Tuvalu",
        "country_code": "TUV",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "USSR",
        "country_code": "SUN",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Uganda",
        "country_code": "UGA",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Ukraine",
        "country_code": "UKR",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "United Arab Emirates",
        "country_code": "UAE",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "United Kingdom of Great Britain and Northern Ireland",
        "country_code": "GBR",
        "region_code": "150",
        "region_code_en": "Europe"
    },
    {
        "name_en": "United Republic of Tanzania",
        "country_code": "TAN",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "United States Virgin Islands",
        "country_code": "VIR",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "United States of America",
        "country_code": "USA",
        "region_code": "021",
        "region_code_en": "Northern America"
    },
    {
        "name_en": "Uruguay",
        "country_code": "URU",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Uzbekistan",
        "country_code": "UZB",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Vanuatu",
        "country_code": "VAN",
        "region_code": "009",
        "region_code_en": "Oceania"
    },
    {
        "name_en": "Venezuela (Bolivarian Republic of)",
        "country_code": "VEN",
        "region_code": "419",
        "region_code_en": "Latin America and the Caribbean"
    },
    {
        "name_en": "Viet Nam",
        "country_code": "SRV",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Western Sahara",
        "country_code": "WSH",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Yemen",
        "country_code": "YEM",
        "region_code": "142",
        "region_code_en": "Asia"
    },
    {
        "name_en": "Zaire",
        "country_code": "ZAR",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Zambia",
        "country_code": "ZAM",
        "region_code": "002",
        "region_code_en": "Africa"
    },
    {
        "name_en": "Zimbabwe",
        "country_code": "ZIM",
        "region_code": "002",
        "region_code_en": "Africa"
    }
]

df = pd.DataFrame.from_records(clist)

#print(df)

df.to_csv("country_list.csv",index=False)