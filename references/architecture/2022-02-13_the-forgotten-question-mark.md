# The forgotten question mark

![question.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/question.2e16d0ba.fill-800x240.png)

Ya know, I love me a question mark. The elegant sickle like curve and dangling dot, those little paired words of how? and why? It's much nicer than a full stop (or period for my American colleagues). Why do IT professionals seem to prefer the latter?

There is a Proof of Concept below the rant - I beg your indulgence dear reader. The PoC uses Kafka and python to transfer files based on the argument laid out below. The GitHub project is here: [mft-kafka](https://github.com/Semprini/mft-kafka)

---

Is it that IT professionals feel that not knowing something makes them less? Is it always the competition, power struggle and politics which stops us engaging openly with different ideas or a different way of doing something?

Often we keep our focus solely on the project, we never ask what does good look like?, what needs to be true to make that good into reality and and just as importantly, how do we pragmatically implement that in the context of my time frames and skills available to implement?

I hate the logical fallacy of Argument from Authority but when no one is willing to engage with the simplest of questions, how does an architect inspire change in the business? I know my shit when it comes to integration - development, architecture and strategy but an architect should not have to build code to get engagement on a solution discussion.

I'm desperately trying to wean my company off batch integration but every project comes with the same arguments around time and cost. My assertion and reply is that streaming, in a like for like comparison with managed file transfers need be no more effort, time or cost.

But Semprini, you perplexing sultan of silicon, you exclaim. All you're suggesting is nothing more than an inefficient method of copying files! Yes indeed dear reader, I am, and I hope that why? that I'm so fond of is ready to hand.

---

I separate data into two: Significant and Non-Significant (insignificant seems a little pejorative to me). We can decide significance using things like reusability, criticality, personally identifiable etc.

In an event driven architecture, any data that is significant should be streamed. Non-significant data can use point to point integration via file transfer - fine with me, fill your boots. This is why it's so important to look at the logical semantics of the data rather than just a data pipeline technology view.

We stream the data so we can apply in-line data quality, and governance, rejecting bad data from the stream into a pool where it can't contaminate down-stream lakes and waterways. Once the data has been filtered we unlock it and put it back in the stream. This allows clean data events to trigger business processes.

However, a project may not have the time or budget to implement a loosely coupled integration, and this is where an architect should put on their thinking shoes and inspiration hat.

If we look at the drivers of an organisation, it is very difficult to deprecate a solution which is providing value to a business group. Extending a solution to provide new value is a much better way for us to implement change. Therefore, if I'm also right with my statement that streaming is no more effort than managed file transfer, it follows that we should use streaming technology for file transfer of significant data. This proof is the point of this PoC.

---

Boilerplate. It's a very utilitarian word hiding a very elegant and powerful tool. Microservices and boilerplate go together like programmers and caffeine. All the key controls that we get with an off the shelf app plus implementation and regression tests of a pattern can be built into microservice boilerplate. Assuming we're not writing the first microservice for the organisation which communicates via streaming then we must have some code we can use as microservice boilerplate. Let's go with the most common that I find: Java and Kafka.

Now I'm also making the assumption that we are creating a managed file transfer job by writing a job configuration in a text file and then putting that through a delivery pipeline, just like code. If not - the principle is cattle not pets, so please sort that out.

Therefore, the overhead of delivery pipelines is the same and for the rest we simply look at some documentation for Confluents Kafka file stream connectors and find it's mimicking the configuration of a managed file transfer config - just split into two files:

File source:

`name=local-file-source  
connector.class=FileStreamSource  
tasks.max=1  
file=/tmp/test.txt  
topic=connect-test`

File sync:

`name=local-file-sink  
connector.class=FileStreamSink  
tasks.max=1  
file=/tmp/test.sink.txt  
topics=connect-test`

Case proven with some pretty reasonable assumptions.

---

I'm not a Java guy any more so I'll write some Python but the principle is the same.

docker-compose Kafka cluster: [source](https://github.com/Semprini/semprini-blog-filekafkatransport/blob/main/kafka/docker-compose.yml)

csv\_producer.py: [source](https://github.com/Semprini/semprini-blog-filekafkatransport/blob/main/csv_producer/csv_producer.py)

Dockerfile: [source](https://github.com/Semprini/semprini-blog-filekafkatransport/blob/main/csv_producer/Dockerfile)

I'm assuming that the container environment can reach to where the source file is located. We should map a volume to this location when running the docker container. The pod/container boilerplate should take care of logging, restarts, alerting etc.

The producer uses the solid watchdog library to wait for file close events to trigger.

`self.event_handler = watchdog.events.PatternMatchingEventHandler(patterns=["*.csv", ],  
 ignore_patterns=[], ignore_directories=True)  
self.event_handler.on_closed = self.on_closed  
self.observer = Observer()  
self.observer.schedule(self.event_handler, self.path, recursive=False)  
self.observer.start()`

On trigger we:

- Grab the modified time

`mtime = os.stat(file_name).st_mtime`

- Read file line by line (I'm assuming a delimited text file) into a dictionary

`dict_reader = csv.DictReader(csvfile)  
 for row in dict_reader:`

- Add the modified time to the dictionary

`row['modified'] = f"{mtime}"`

- Write each dictionary as JSON to a Kafka topic

`self.producer.send(topic_name, value=row)`

- Once all lines have been sent, we send an audit record to an audit Kafka topic

`audit_record = {  
 "file_name": f"{file_name}",  
 "topic_name": f"{topic_name}",  
 "modified": f"{mtime}",  
 "row_count": f"{row_count}",  
        }  
 self.producer.send(self.topic_audit, value=audit_record)  
 self.producer.flush()`

The result is a csv producer which de-batches and streams to a kafka topic named for the file based on file change events.

The consumer is triggered by the audit records - I.e. the complete file has been streamed and it uses this to confirm that all records have arrived. Simple read of the stream, append to a file and close the file once all records have been written.

---

We can now extend the solution at our leisure by building canonical transformations from the source stream without affecting the projects file transfer and therefore we're closer to our strategic event driven architecture.

I quite like the 2 microservices. I like being able to be a bit more opinionated than the file stream connectors to deliver a useful utility so I'll be replacing the code with something production ready - buffering, testing, chunking etc.
