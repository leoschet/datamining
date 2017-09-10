import main

queries = [
    {
        'query': 'Creating and destroying objects',
        'checker_file': '../res/queries/Query - Creating and destroying objects.txt'
    },
    {
        'query': 'Mixing and playing audio',
        'checker_file': '../res/queries/Query - Mixing and playing audio.txt'
    }
]

rankers = main.get_default_rankers()
check_sizes = [5, 10, 20, 50, 100]
relevancy_threshold = 0.2

for query_info in queries:
    print('query: %s' % query_info['query'])

    print('reading query manual classification file')
    print('relevancy threshold set to %f' % relevancy_threshold)
    relevant_documents = {None}
    for line in open(query_info['checker_file']):
        if line.startswith('#') or len(line) < 5:
            continue
        line_data = line.split(' - ')
        if float(line_data[0]) > relevancy_threshold:
            relevant_documents.add(line_data[1].strip('\n').strip(' '))
    print('total relevant documents is %d' % len(relevant_documents))

    print('executing query in all rankers')
    search_results = main.search_query(query_info['query'], rankers, True)[0]

    for ranker_name in search_results:
        print('ranker %s' % ranker_name)
        result = search_results[ranker_name]
        for check_size in check_sizes:
            print('check size: %d' % check_size)
            relevant_documents_in_search_count = 0.0
            for i in range(check_size):
                if result[i][0] in relevant_documents:
                    relevant_documents_in_search_count += 1
            print('relevant documents in search: %d' % relevant_documents_in_search_count)
            precision = relevant_documents_in_search_count / check_size
            print('precision: %f' % precision)
            recall = relevant_documents_in_search_count / len(relevant_documents)
            print('recall %f' % recall)
            f_measure = 2 * precision * recall / (precision + recall)
            print('f-measure: %f' % f_measure)
            print()
    print()
    print()
