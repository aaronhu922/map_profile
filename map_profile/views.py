import logging
import re

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from io import open
import os
import pdfplumber

from .map_res_table import draw_map_table
from .models import EarlyliteracySkillSetScores, MapTestCheckItem
from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
from .parse_helper import ExtractStarData, extract_map_data
from .star_reading_table import draw_star_reading_table

log = logging.getLogger("map_test")


# Create your views here.
@csrf_exempt
def choose_file(request):
    temp = loader.get_template('pdf2MySQL/upload_file.html')
    return HttpResponse(temp.render())


@csrf_exempt
def upload_file(request):
    return render(request, 'pdf2MySQL/upload_file.html')


@csrf_exempt
def handle_pdf_data(request):
    # request.Files['myfile']
    if 'phone_number' not in request.POST:
        return JsonResponse({"errorCode": "400",
                             "executed": True,
                             "message": "No phone number input for pdf upload!",
                             "success": False}, status=200)

    phonenumber = request.POST['phone_number']
    test_type = request.POST['test_type']
    '''  3 types of test report.
    "star_early", "star_reading", "map_test"
    '''
    log.warning("Import {} report for user {}".format(test_type, phonenumber))
    if not phonenumber:
        return JsonResponse({"errorCode": "400",
                             "executed": True,
                             "message": "No phone number input for pdf upload!",
                             "success": False}, status=200)

    if request.method == 'POST':  # 请求方法为POST时，进行处理
        try:
            myFile = request.FILES['myfile']  # 获取上传的文件，如果没有文件，则默认为None
            ext_file = request.FILES['ext_file']
        except MultiValueDictKeyError as err:
            log.warning(err)
            return JsonResponse({"errorCode": "400",
                                 "executed": True,
                                 "message": "Need to choose a PDF file for upload. {}!".format(err),
                                 "success": False}, status=200)
        if not myFile:
            return JsonResponse({"errorCode": "400",
                                 "executed": True,
                                 "message": "No file was uploaded!",
                                 "success": False}, status=200)

        destination = open(os.path.join(settings.MEDIA_ROOT, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作

        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)

        destination.close()

        ################################################################
        #  trans to txt file and stored in txtintermediate dictionary
        ################################################################
        pdffilestored = os.path.join(settings.MEDIA_ROOT, myFile.name)

        # with pdfplumber.open(pdffilestored) as pdf:
        #     content = ''
        #     # len(pdf.pages)为PDF文档页数
        #     for i in range(len(pdf.pages)):
        #         # pdf.pages[i] 是读取PDF文档第i+1页
        #         page = pdf.pages[i]
        #         # page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
        #         page_content = '\n'.join(page.extract_text().split('\n')[1:-1])
        #         content = content + page_content
        # print(content)

        # with pdfplumber.open(ext_file) as pdf2:
        #     content = ''
        #     # len(pdf.pages)为PDF文档页数
        #     for i in range(len(pdf2.pages)):
        #         # pdf.pages[i] 是读取PDF文档第i+1页
        #         page = pdf2.pages[i]
        #         # page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
        #         page_content = '\n'.join(page.extract_text().split('\n')[1:-1])
        #         content = content + page_content
        #     print(content)

        with pdfplumber.open(ext_file) as pdf1:
            content = ''
            pages = pdf1.pages
            tbl = pages[0].extract_tables()
            print(tbl)
            print(tbl[0][-2])
            data = str(tbl[0][-2])
            data = data.replace('\\n', '&')
            data = data.replace('\\uf120', '---')
            print(data)
            #             data = '''
            # 'COMPARISONS&GROWTH & ACHIEVEMENT MEASURES&Norms Percentile&GROWTH ACHIEVEMENT&- - Above Mean&No growth tests available&81 ST&Quadrant Chart&- -&No growth tests available&PROJECTIONS&No projections available&READABILITY MEASURES&Lexile* Flesch-Kincaid Grade Level&570L - 720L 3.5 to 4.2', '', 'INSTRUCTIONAL AREAS&193 Vocabulary Use and Functions&---Relative Strength&196 Language and Writing&---Relative Strength&201 Foundational Skills&---Relative Strength&208 Literature and Informational Text&---Relative Strength', '', 'GROWTH GOALS&SPRING 2021&Customize the growth target for this student&\uf106&by setting a growth goal&Past Goals&There are no previous goals for this student.'INSTRUCTIONAL AREAS&Literary Text: Language, Craft, and&185&Structure&---Relative Strength&185 Vocabulary: Acquisition and Use&---Relative Strength&Informational Text: Language, Craft,&197&and Structure---Relative Strength&199 Literary Text: Key Ideas and Details&---Relative StrengthInformational Text: Key Ideas and&203&Details&---Relative Strength&''INSTRUCTIONAL AREAS&Writing: Write, Revise Texts for&213&Purpose and Audience&---Relative Strength&Language: Understand, Edit for&218&Mechanics---Relative Strength&Language: Understand, Edit for&223&Grammar, Usage&---Relative Strength', '', 'GROWTH GOALS&SPRING 2021&Customize the growth target for this student&\uf106&by setting a growth goal&Past Goals&There are no previous goals for this student.'                  '''

            regex1 = '&(\d+ (TH|RD|ST|ND))&'
            regex2 = '\d\.\d to \d\.\d'
            regex3 = '\d+L - \d+L'
            regex4 = 'GROWTH GOALS&([\w ]+)'
            value1 = re.search(regex1, data)
            value2 = re.findall(regex2, data)
            value3 = re.findall(regex3, data)
            value4 = re.findall(regex4, data)

            if value1:
                print(value1.group())
                print(value1.group().strip('&'))
            if value2:
                print(value2[0])
            if value3:
                print(value3[0])
            if value4:
                print(value4[0])
            # domain_list_one_line = ['Literary Text: Key Ideas and Details',
            #                         'Vocabulary: Acquisition and Use',
            #                         'Vocabulary Use and Functions',
            #                         'Language and Writing',
            #                         'Foundational Skills',
            #                         'Literature and Informational Text',
            #                         ]
            # domain_list_two_lines = [
            #     'Informational Text: Language, Craft,',
            #     'Literary Text: Language, Craft, and',
            #     'Informational Text: Key Ideas and',
            #     'Writing: Write, Revise Texts for',
            #     'Language: Understand, Edit for'
            # ]
            domain_name_reg_list = ['Literary Text: Key Ideas and Details',
                                    'Informational Text: Language, Craft,[\d&]+and Structure',
                                    'Literary Text: Language, Craft, and[\d&]+Structure',
                                    'Vocabulary: Acquisition and Use',
                                    'Informational Text: Key Ideas and[\d&]+Details',
                                    'Vocabulary Use and Functions',
                                    'Language and Writing',
                                    'Foundational Skills',
                                    'Literature and Informational Text',
                                    'Writing: Write, Revise Texts for[\d&]+Purpose and Audience',
                                    'Language: Understand, Edit for[\d&]+Mechanics',
                                    'Language: Understand, Edit for[\d&]+Grammar, Usage'
                                    ]
            full_domain_list = ['Literary Text: Key Ideas and Details',
                                'Informational Text: Language, Craft, and Structure',
                                'Literary Text: Language, Craft, and Structure',
                                'Vocabulary: Acquisition and Use',
                                'Informational Text: Key Ideas and Details',
                                'Vocabulary Use and Functions',
                                'Language and Writing',
                                'Foundational Skills',
                                'Literature and Informational Text',
                                'Writing: Write, Revise Texts for Purpose and Audience',
                                'Language: Understand, Edit for Mechanics',
                                'Language: Understand, Edit for Grammar, Usage'
                                ]
            for i in range(len(domain_name_reg_list)):
                reg_focus = '(' + domain_name_reg_list[i] + ')[&]?---[&]?Suggested Area of Focus'
                reg_strength = '(' + domain_name_reg_list[i] + ')[&]?---[&]?Relative Strength'
                for domain in re.findall(reg_focus, data):
                    name = re.sub("&[\\d&]*", " ", domain).strip()
                    print("Focus: " + name)
                    print("Index: {}".format(i))
                for domain in re.findall(reg_strength, data):
                    name = re.sub("&[\\d&]*", " ", domain).strip()
                    print("Strength: " + name)
                    print("Index: {}".format(i))
            # for item in domain_list_one_line:
            #     reg_focus = '(' + item + '[ \d\w,]*)[&]?---[&]?Suggested Area of Focus'
            #     reg_strength = '(' + item + '[ \d\w,]*)[&]?---[&]?Relative Strength'
            #     for domain in re.findall(reg_focus, data):
            #         name = re.sub("&[\\d&]*", " ", domain).strip()
            #         print("Focus: " + name)
            #         print("Index: {}".format(full_domain_list.index(name)))
            #     for domain in re.findall(reg_strength, data):
            #         name = re.sub("&[\\d&]*", " ", domain).strip()
            #         print("Strength: " + name)
            #         print("Index: {}".format(full_domain_list.index(name)))

        ################################################################
        #  trans end
        ################################################################
    try:
        if test_type == "star_early":
            ExtractStarData(content, phonenumber)
        elif test_type == "map_test":
            # stu_map_pro = extract_map_data(content, phonenumber)
            # draw_map_table(stu_map_pro)
            print("map test!")
        elif test_type == "star_reading":
            draw_star_reading_table()
        else:
            raise
    except Exception as err:
        log.error(err)
        log.error("Upload pdf {} failed!".format(myFile.name))
        temp = loader.get_template('pdf2MySQL/show_failed.html')
        raise
    else:
        temp = loader.get_template('pdf2MySQL/show_success.html')

    os.remove(pdffilestored)
    # os.remove(txtfilestored)
    return HttpResponse(temp.render())


def show(self, request):
    temp = loader.get_template('pdf2MySQL/show_success.html')
    return HttpResponse(temp.render())


# @login_required
# @ensure_csrf_cookie
@csrf_exempt
def get_student_exam_stats(request, phone):
    if request.method == 'GET':
        instance = list(EarlyliteracySkillSetScores.objects.filter(phone_number=phone).order_by('-TestDate')[:3])
        log.warning("Get {} test results for user {}".format(len(instance), phone))
        if not instance or len(instance) <= 0:
            return JsonResponse({"errorCode": "400",
                                 "executed": True,
                                 "message": "User with phone {} does not have any test result!".format(phone),
                                 "success": False}, status=200)
        else:
            scaled_score = instance[0].ScaledScore
            lexile_measure = instance[0].LexileMeasure
            test_date = instance[0].TestDate

            sub_items_alphabetic_principle = [instance[0].AlphabeticKnowledge,
                                              instance[0].AlphabeticSequence,
                                              instance[0].LetterSounds,
                                              instance[0].PrintConceptsWordLength,
                                              instance[0].PrintConceptsWordBorders,
                                              instance[0].PrintConceptsLettersAndWords,
                                              instance[0].Letters,
                                              instance[0].IdentificationAndWordMatching]

            sub_items_phonemic_awareness = [instance[0].RhymingAndWordFamilies,
                                            instance[0].BlendingWordParts,
                                            instance[0].BlendingPhonemes,
                                            instance[0].InitialAndFinalPhonemes,
                                            instance[0].ConsonantBlendsPA,
                                            instance[0].MedialPhonemeDiscrimination,
                                            instance[0].PhonemeIsolationORManipulation,
                                            instance[0].PhonemeSegmentation]

            sub_items_phonics1 = [instance[0].ShortVowelSounds,
                                  instance[0].InitialConsonantSounds,
                                  instance[0].FinalConsonantSounds,
                                  instance[0].LongVowelSounds,
                                  instance[0].VariantVowelSounds,
                                  instance[0].ConsonantBlendsPH]

            sub_items_phonics2 = [instance[0].ConsonantDigraphs,
                                  instance[0].OtherVowelSounds,
                                  instance[0].SoundSymbolCorrespondenceConsonants,
                                  instance[0].WordBuilding,
                                  instance[0].SoundSymbolCorrespondenceVowels,
                                  instance[0].WordFamiliesOrRhyming]

            sub_items_structural_vocabulary = [instance[0].WordsWithAffixes,
                                               instance[0].Syllabification,
                                               instance[0].CompoundWords,
                                               instance[0].WordFacility,
                                               instance[0].Synonyms,
                                               instance[0].Antonyms]

            sub_items_other_domains = [instance[0].ComprehensionATtheSentenceLevel,
                                       instance[0].ComprehensionOfParagraphs,
                                       instance[0].NumberNamingAndNumberIdentification,
                                       instance[0].NumberObjectCorrespondence,
                                       instance[0].SequenceCompletion,
                                       instance[0].ComposingAndDecomposing,
                                       instance[0].Measurement]

            # sub_domain_score = [instance[0].AlphabeticPrinciple, instance[0].ConceptOfWord,
            #                     instance[0].VisualDiscrimination,
            #                     instance[0].Phonics, instance[0].StructuralAnalysis, instance[0].Vocabulary,
            #                     instance[0].SentenceLevelComprehension, instance[0].PhonemicAwareness,
            #                     instance[0].ParagraphLevelComprehension, instance[0].EarlyNumeracy]

            sub_domain_score_trend_date = []
            sub_domain_score_trend_value = []

            for result in reversed(instance):
                sub_domain_score_trend_date.append(result.TestDate)
                sub_domain_score_data = [
                    round((result.AlphabeticPrinciple + result.ConceptOfWord + result.VisualDiscrimination) / 3, 1),
                    result.PhonemicAwareness, result.Phonics, (result.StructuralAnalysis + result.Vocabulary) / 2,
                    round((
                                  result.SentenceLevelComprehension + result.ParagraphLevelComprehension + result.EarlyNumeracy) / 3,
                          1)]
                sub_domain_score_trend_value.append(sub_domain_score_data)

            return JsonResponse({
                "test_date": test_date,
                "lexile_measure": lexile_measure,
                "scaled_score": scaled_score,
                "sub_items_alphabetic_principle": sub_items_alphabetic_principle,
                "sub_items_phonemic_awareness": sub_items_phonemic_awareness,
                "sub_items_phonics1": sub_items_phonics1,
                "sub_items_phonics2": sub_items_phonics2,
                "sub_items_structural_vocabulary": sub_items_structural_vocabulary,
                "sub_items_other_domains": sub_items_other_domains,
                "sub_domain_score_trend_date": sub_domain_score_trend_date,
                "sub_domain_score_trend_value": sub_domain_score_trend_value,
                "errorCode": "200",
                "executed": True,
                "message": "Succeed to get latest test result of user {}!".format(phone),
                "success": True
            }, status=200)
