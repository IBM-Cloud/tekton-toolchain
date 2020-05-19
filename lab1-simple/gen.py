import click
from totkn import *


def document_out(tkn) -> str:
    return "---\n" + tkn.to_yaml()


def gen():
    steps = [
        Step(image="ubuntu", name="echo", command=["echo"], args=["01 version"]),
        Step(image="ubuntu", name="lslslash", command=["ls"], args=["-l", "/"]),
        Step(image="ubuntu", name="lsl-ubuntu", command=["ls"], args=["-l"]),
        Step(image="ubuntu", name="pwd", command=["pwd"]),
        Step(image="ubuntu", name="ls", command=["ls"]),
        Step(image="ubuntu", name="env", command=["env"]),
        Step(
            image="ubuntu",
            name="write",
            command=["/bin/bash"],
            args=["-c", "echo stuff > file; ls; cat file"],
        ),
        Step(image="ubuntu", name="lsafter", command=["ls"], args=["-l"]),
    ]
    t = Task(name="the-task", steps=steps)
    p = Pipeline(name="pipeline", tasks=[PipelineTask("xx1", taskRef=t.ref())])
    tt = TriggerTemplate(name="theTemplateTrigger")
    pipeline_run = PipelineRun(name="pipelinerun-$(uid)")
    pipeline_run.pipelineRef = p.ref()
    tt.resourcetemplates = [pipeline_run]
    tb = TriggerBinding("theTriggerBinding")
    el = EventListener("the-listener")
    el.triggers = [EventListenerTrigger(binding=tb.ref(), template=tt.ref())]
    # dump out the file
    ret = document_out(el)
    ret += document_out(tb)
    ret += document_out(tt)
    ret += document_out(p)
    ret += document_out(t)
    return ret


if __name__ == "__main__":
    click.echo(gen())
